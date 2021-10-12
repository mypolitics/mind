from moviepy.editor import VideoFileClip
import os

def cut_last_sec(path: str, sec: int):

    video = VideoFileClip(path)

    filename = f'{os.path.splitext(video.filename)[0]}#Short.mp4'

    clip = video.subclip(0, video.duration - sec)
    clip.write_videofile(filename)

    video.close()

    os.remove(path)

    return filename

