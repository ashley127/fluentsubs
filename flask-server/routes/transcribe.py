from flask import Blueprint, request, jsonify, session, Response
import torch
import os
import subprocess
import soundfile as sf
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

# Set up the blueprint
transcribe_bp = Blueprint('transcribe', __name__)

# Set device to MPS if available (for M1 chip)
device = "mps" if torch.backends.mps.is_available() else "cpu"
torch_dtype = torch.float32

model_id = "distil-whisper/distil-large-v3"

# Load the model and processor
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

def format_time(seconds):
    """Convert seconds to the SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt(chunks):
    print("starting to generate")
    """Generate SRT content from segments."""
    srt_content = ""
    for i, chunk in enumerate(chunks):
        print(chunk)
        
        start_time = format_time(chunk['start_time'])
        end_time = format_time(chunk['end_time'])
        text = chunk['text']
        
        srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"
        print(f"processing {i} chunk")
    
    return srt_content


def convert_to_mp3(file_path, output_path):
    """Convert a file to MP3 using FFmpeg."""
    command = [
        'ffmpeg',
        '-i', file_path,
        '-q:a', '0',
        '-map', 'a',
        output_path
    ]
    subprocess.run(command, check=True)

def convert_to_mono(input_file, output_file):
    """Convert audio to mono channel using FFmpeg."""
    command = [
        'ffmpeg',
        '-i', input_file,
        '-ac', '1',  # Set audio channels to 1 (mono)
        '-c:a', 'pcm_s16le',  # Use PCM audio codec for WAV format
        output_file
    ]
    subprocess.run(command, check=True)

@transcribe_bp.route('/transcribe-file/<file_id>', methods=['POST'])
def transcribe_file(file_id):
    try:
        # Find the correct file extension
        files = session.get('files', [])
        file_info = next((file for file in files if file['id'] == file_id), None)
        if not file_info:
            return f"File not found in session.", 404

        original_filename = file_info['name']
        file_extension = os.path.splitext(original_filename)[1]
        file_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}{file_extension}'

        # Determine if the file is already an MP3
        if file_extension.lower() != '.mp3':
            audio_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}.mp3'
            convert_to_mp3(file_path, audio_path)
        else:
            audio_path = file_path

        # Convert audio to mono
        mono_audio_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}_mono.wav'
        convert_to_mono(audio_path, mono_audio_path)

        # Load the audio file
        waveform, sample_rate = sf.read(mono_audio_path)

        # Process the audio with the pipeline
        result = pipe({"array": waveform, "sampling_rate": sample_rate})

        # Debug: Print the full result from the pipeline
        print("Pipeline Result:", result)

        # Extract text and timestamps
        transcription_text = result.get("text", "")
        chunks = result.get("chunks", [])  # Use "chunks" instead of "segments"

        # Debug: Print segments to check their content
        print("Chunks:", chunks)

        # Prepare segment data
        formatted_chunks = []
        for chunk in chunks:
            print(chunk)
            start_time = chunk.get("timestamp", (0, 0))[0]  # Start time of the segment in seconds
            end_time = chunk.get("timestamp", (0, 0))[1]    # End time of the segment in seconds
            text = chunk.get("text", "")                    # Transcribed text for the segment

            formatted_chunks.append({
                "start_time": start_time,
                "end_time": end_time,
                "text": text
            })


        # Generate SRT content
        srt_content = generate_srt(formatted_chunks)

        # Debug: Print SRT content to check its format
        print("SRT Content:", srt_content)

        # Save the SRT file
        srt_filename = f"{file_id}.srt"
        srt_filepath = os.path.join("/Users/danielzhao/Documents/Github/fluentsubs/flask-server/srt_files", srt_filename)
        with open(srt_filepath, "w") as srt_file:
            srt_file.write(srt_content)

        # Store the transcription with timestamps in the session
        transcriptions = session.get('transcriptions', {})
        transcriptions[file_id] = {
            "text": transcription_text,
            "segments": formatted_chunks
        }
        session['transcriptions'] = transcriptions

        return jsonify({"transcription": transcription_text, "srt_file": srt_filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
