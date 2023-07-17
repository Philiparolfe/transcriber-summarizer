from pydub import AudioSegment
import openai


# Dont forget to enter API key
from keys import MY_KEY
openai.api_key = MY_KEY

# PyDub handles time in milliseconds
ten_minutes = 10 * 60 * 1000

def segment_audio(file_name: str) -> str:
    audio_file = AudioSegment.from_wav(file_name)
    first_10_minutes = audio_file[:ten_minutes]
    first_10_minutes.export(f"{file_name}_10.wav", format="wav")
    return f"{file_name}_10.wav"


# Whiper API :

def whisper_transcribe(audio_file: str) -> str:
    audio_file = open(audio_file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]