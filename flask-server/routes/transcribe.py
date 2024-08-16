from flask import Blueprint, request, jsonify
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import soundfile as sf
from pydub import AudioSegment
import io

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

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Load the MP3 file and convert it to a WAV format
        audio = AudioSegment.from_file(file, format="mp3")
        wav_file = io.BytesIO()
        audio.export(wav_file, format="wav")

        # Load the WAV file using soundfile
        wav_file.seek(0)
        waveform, sample_rate = sf.read(wav_file)

        # Process the audio with the pipeline
        result = pipe({"array": waveform, "sampling_rate": sample_rate})

        return jsonify({'transcription': result["text"]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
