from flask import Blueprint, request, jsonify, session
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
    chunk_length_s=15,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)

def generate_srt(chunks):
    """Generate SRT content from segments."""
    srt_content = ""
    prev_time = 0
    total_time = 0

    def format_time(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    for i, chunk in enumerate(chunks):
        start_seconds = chunk['start_time']
        end_seconds = chunk['end_time']

        if prev_time >= end_seconds:
            # total_time += prev_time
            total_time += 15 # match the chunk length
        prev_time = end_seconds

        start_seconds += total_time
        end_seconds += total_time

        start_time = format_time(start_seconds)
        end_time = format_time(end_seconds)
        text = chunk['text']

        srt_content += f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n"

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
            return "File not found in session.", 404

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

        # Extract text and timestamps
        transcription_text = result.get("text", "")
        chunks = result.get("chunks", [])

        # Prepare segment data
        formatted_chunks = []
        for chunk in chunks:
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

        # Save the SRT file to the specified directory
        srt_directory = '/Users/danielzhao/Documents/Github/fluentsubs/flask-server/srt_files'
        os.makedirs(srt_directory, exist_ok=True)
        srt_file_path = os.path.join(srt_directory, f"{file_id}.srt")
        with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)

        # Save the transcription in the session
        transcriptions = session.get('transcriptions', {})
        transcriptions[file_id] = transcription_text
        session['transcriptions'] = transcriptions

        # Return success response
        return {"status_code": 200, "srt_file_path": srt_file_path}

    except Exception as e:
        return {"status_code": 500}
