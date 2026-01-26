from faster_whisper import WhisperModel


def transcribe_ad(audio_path, transcript_path):
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path)

    with open(transcript_path, "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(segment.text + "\n")


transcribe_ad(
    r" ", # Path to the audio file
    r" " # Path to save the transcript file
)
