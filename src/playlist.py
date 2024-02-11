import datetime
import os
import isodate
from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY_YT_LEARN')


class PlayList:
    """Класс для статистики плейлиста"""

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.playlist = (self.youtube.playlistItems().list(playlistId=self.pl_id,
                                                           part='contentDetails,snippet').execute())
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = "https://www.youtube.com/playlist?list=" + "PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
        self.videos_id: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]

    def video_response(self) -> dict:
        """Информация о видео для дальнейшей обработки"""
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.videos_id)
                                                    ).execute()
        return video_response

    @property
    def total_duration(self) -> datetime.timedelta:
        """Общая продолжительность плейлиста в секундах"""
        total_duration = datetime.timedelta()
        for video in self.video_response()['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += datetime.timedelta(seconds=duration.total_seconds())
        return total_duration

    def show_best_video(self) -> str:
        """Показывает топ видео по лайкам из плейлиста."""
        best_video_id = ''
        more_like = 0
        for video in self.video_response()['items']:
            like_count: int = video['statistics']['likeCount']
            video_id = video['id']
            if int(like_count) > int(more_like):
                more_like = like_count
                best_video_id = video_id
        return f"https://youtu.be/{best_video_id}"
