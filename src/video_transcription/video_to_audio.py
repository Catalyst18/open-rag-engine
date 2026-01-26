#this file is used to convert video files to audio files

from moviepy import VideoFileClip

def convert_video_to_audio(video_path, output_audio_path):
    video_path=r""
    output_audio_path=r""

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