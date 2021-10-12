from googleapiclient.http import MediaFileUpload


class UploadVideo:

    def __init__(self, service, info: dict, file_path: str):
        self.service = service
        self.info = info
        self.file_path = file_path

    def get_body(self):
        return {
            'snippet': {
                'title': f'{self.info["snippet"]["title"]}| #Short',
                'description': f'{self.info["snippet"]["description"]}| #Short',
            },
            'status': {
                'privacyStatus': 'private',
            }
        }

    def get_file(self):
        return MediaFileUpload(self.file_path)

    def upload(self):
        response = self.service.videos().insert(
            part='snippet,status',
            body=self.get_body(),
            media_body=self.get_file()
        ).execute()

        return response
