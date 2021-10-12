import random
import pickle
import os
from dotenv import dotenv_values

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from moduls import download, cut_video
from moduls.upload_video import UploadVideo
from moduls.send_mess import SendMessage

config = dotenv_values(".env")

VIDEOS_COUNT = 20
BASE_VIDEO_PATH = 'https://www.youtube.com/watch?v='
client_secret_file = "client_secrets.json"

credentials = None

if os.path.exists('token.pickle'):
    print('Loading Credentials From File...')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file,
            scopes=["https://www.googleapis.com/auth/youtube.readonly",
                    "https://www.googleapis.com/auth/youtube.upload"]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

youtube = build('youtube', 'v3', credentials=credentials)

# GET FROM YT
request_video_by_relevance = youtube.search().list(
    part="snippet",
    channelId=config.get('channel_id'),
    maxResults=VIDEOS_COUNT,
    order="relevance"
)
video_by_relevance = request_video_by_relevance.execute()

random_video = random.sample(video_by_relevance['items'], 3)

send_message = SendMessage(config.get('webhook_url'))

for video in random_video:
    video_path = download.download_by_id(video['id']['videoId'])
    edited_video_path = cut_video.cut_last_sec(video_path, 5)

    upload_video = UploadVideo(youtube, video, edited_video_path)

    response = upload_video.upload()

    send_message.send_new_video_alert(response)
