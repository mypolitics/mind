import sqlite3


class DB:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS uploaded_video (
                videoId text PRIMARY KEY,
                title text NOT NULL,
                channelId text NOT NULL
            )''')

    def __del__(self):
        print('save data')
        self.con.commit()

    def video_exist(self, video_id: str):
        data = self.cur.execute("SELECT * FROM uploaded_video WHERE videoId= ?", (video_id,)).fetchone()

        return data

    def add_video(self, video: dict):
        videoId = video['id']['videoId']
        title = video['snippet']['title']
        channelId = video['snippet']['channelId']

        self.cur.execute("INSERT INTO uploaded_video VALUES (?, ?, ?)", (videoId, title, channelId,))
