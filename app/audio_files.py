import whisper
from summarization import generate_summary

model2 = whisper.load_model("base")

def process_audio_file(audio_path):
    result = model2.transcribe(audio_path)
    text = result["text"]
    summary = generate_summary(text)
    return summary



# audio = "temp/0.wav"
# text = audio_to_video(audio)
# print(generate_summary(text))    