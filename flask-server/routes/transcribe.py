from flask import Blueprint, request, jsonify, session
import torch
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
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device,
)

@transcribe_bp.route('/transcribe-file/<file_id>', methods=['POST'])
def transcribe_file(file_id):
    try:
        # Assuming the file has already been downloaded locally for processing
        file_path = f'/Users/danielzhao/Documents/Github/fluentsubs/flask-server/file_downloads/{file_id}.mp3'
        
        # Load the audio file
        waveform, sample_rate = sf.read(file_path)

        # Process the audio with the pipeline
        result = pipe({"array": waveform, "sampling_rate": sample_rate})

        # Store the transcription in the session or return it directly
        transcription_text = result["text"]
        transcriptions = session.get('transcriptions', {})
        transcriptions[file_id] = transcription_text
        session['transcriptions'] = transcriptions

        return jsonify({"transcription": transcription_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
