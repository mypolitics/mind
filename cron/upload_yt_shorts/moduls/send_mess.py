import requests


class SendMessage:

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_new_video_alert(self, video_data: dict):
        print(video_data)
        data = {
            "embeds": [{
                "title": f"Załadowano nowy film \ntytuł: {video_data['snippet']['title']}",
                "description": f"https://youtu.be/{video_data['id']}"
            }]
        }

        requests.post(self.webhook_url, json=data)
