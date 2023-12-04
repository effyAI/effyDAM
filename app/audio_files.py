import whisper
from summarization import generate_summary

model2 = whisper.load_model("medium")

def process_audio_file(audio_path):
    result = model2.transcribe(audio_path, fp16 = False)
    text = result["text"]
    summary = generate_summary(text)
    return summary



# audio = "https://effy-voice-dataset.s3.amazonaws.com/468a6991/wav/0.wav"
# text = process_audio_file(audio)
# print(generate_summary(text))    