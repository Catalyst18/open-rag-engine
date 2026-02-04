#this file is used to convert video files to audio files
import os
from moviepy import VideoFileClip

def convert_video_to_audio(video_path, output_audio_path):
    video_path=r"C:\Users\TYSON\Desktop\Projects\old_rag\open-rag-engine\uploaded_videos\short.mp4"
    output_audio_path = r"C:\Users\TYSON\Desktop\Projects\old_rag\open-rag-engine\src\video_transcription\audio\output.mp3"


    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio_path, codec='libmp3lame')
        audio_clip.close()
        video_clip.close()
        print("Conversion successful")
    except Exception as e:
        print(e)
convert_video_to_audio("input_video.mp4", "output_audio.mp3")