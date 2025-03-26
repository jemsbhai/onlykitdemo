import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile

def record_audio(duration=5, samplerate=16000):
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
        wav.write(tmpfile.name, samplerate, recording)
        return tmpfile.name

def transcribe_audio(filename):
    print("Loading Whisper model...")
    model = whisper.load_model("base")  # You can change to 'tiny', 'small', 'medium', 'large'
    print("Transcribing...")
    result = model.transcribe(filename)
    return result["text"]

# if __name__ == "__main__":
#     # audio_file = record_audio(duration=5)
#     # transcript = transcribe_audio(audio_file)
#     # print("Transcribed Text:", transcript)
