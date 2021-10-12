# import json
import random

from googleapiclient.discovery import build
import google_auth_oauthlib.flow
from dotenv import dotenv_values

from moduls import download, cut_video
from moduls.send_mess import SendMessage
from moduls.upload_video import UploadVideo

config = dotenv_values(".env")
send_message = SendMessage(config.get('webhook_url'))

VIDEOS_COUNT = 20
BASE_PATH = 'https://www.youtube.com/watch?v='
scopes = ["https://www.googleapis.com/auth/youtube.upload"]

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secrets.json"


flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()


youtube_api_list = build(api_service_name, api_version, developerKey=config.get('api_key'))
youtube_api_auth = build(api_service_name, api_version, credentials=credentials)

# GET FROM YT
request_video_by_relevance = youtube_api_list.search().list(
    part="snippet",
    channelId=config.get('channel_id'),
    maxResults=VIDEOS_COUNT,
    order="relevance"
)
video_by_relevance = request_video_by_relevance.execute()

# GET FROM JSON
# with open('video_by_relevance.json', 'r') as video_data:
#     video_by_relevance = {'items': json.load(video_data)}
# print(video_by_relevance)

random_video = random.sample(video_by_relevance['items'], 3)

for video in random_video:
    video_path = download.download_by_id(video['id']['videoId'])
    edited_video_path = cut_video.cut_last_sec(video_path, 5)

    upload_video = UploadVideo(youtube_api_auth, video, edited_video_path)

    response = upload_video.upload()

    send_message.send_new_video_alert(response)
