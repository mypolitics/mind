from pytube import YouTube

BASE_LINK = 'https://www.youtube.com/watch?v='
PATH = 'videos'


def download_by_id(video_id: str):
    video_yt = YouTube(BASE_LINK + video_id)
    return video_yt.streams.get_highest_resolution().download(PATH)

