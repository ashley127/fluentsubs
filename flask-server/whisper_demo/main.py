import torch
import soundfile as sf
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from pydub import AudioSegment

# Set device to MPS if available (for M1 chip)
device = "mps" if torch.backends.mps.is_available() else "cpu" # change back to nvidia, cuz mac sucks!
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

# Load your MP3 file and convert it to a WAV format that soundfile can process
audio_file = "sample2.flac"

# Convert MP3 to WAV using pydub
# audio = AudioSegment.from_flac(audio_file)
# wav_file = "temp.wav"
# audio.export(wav_file, format="wav")

# Load the WAV file using soundfile
waveform, sample_rate = sf.read(audio_file)

# Process the audio with the pipeline
result = pipe({"array": waveform, "sampling_rate": sample_rate})

print(result["text"])
