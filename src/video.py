import os

from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY_YT_LEARN')


class Video:
    """Класс для статистики ютуб-видео"""
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, video_id):
        pass
        self.video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=video_id
                                                ).execute()
        self.video_id = video_id
        self.video_title: str = self.video['items'][0]['snippet']['title']
        self.view_count: int = self.video['items'][0]['statistics']['viewCount']
        self.like_count: int = self.video['items'][0]['statistics']['likeCount']
        self.comment_count: int = self.video['items'][0]['statistics']['commentCount']

    def __str__(self):
        """Возвращает название видео"""
        return self.video_title


class PLVideo(Video):
    """Класс для статистики ютуб-видео"""
    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.PL_id = pl_id
