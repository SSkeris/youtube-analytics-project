import json
import os
from pprint import pprint

from googleapiclient.discovery import build

API_KEY: str = os.getenv('API_KEY_YT_LEARN')


class Channel:
    """Класс для ютуб-канала"""
    __youtube = build("youtube", "v3", developerKey=API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def __str__(self):
        """Возвращает название канала и ссылку на канал"""
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return int(self.channel['items'][0]['statistics']["videoCount"]) + int(other.channel['items'][0]['statistics'][
            "videoCount"])

    def __sub__(self, other):
        return int(self.channel['items'][0]['statistics']["videoCount"]) - int(other.channel['items'][0]['statistics'][
            "videoCount"])

    def __gt__(self, other):
        return self.channel['items'][0]['statistics']["videoCount"] > other.channel['items'][0]['statistics'][
            "videoCount"]

    def __ge__(self, other):
        return self.channel['items'][0]['statistics']["videoCount"] >= other.channel['items'][0]['statistics'][
            "videoCount"]

    def __lt__(self, other):
        return self.channel['items'][0]['statistics']["videoCount"] < other.channel['items'][0]['statistics'][
            "videoCount"]

    def __le__(self, other):
        return self.channel['items'][0]['statistics']["videoCount"] <= other.channel['items'][0]['statistics'][
            "videoCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        pprint(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name: str) -> None:
        """метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        data = json.dumps(self.channel)
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(data)

    @property
    def channel_id(self):
        """запрос id канала"""
        return self.__channel_id

    @property
    def title(self):
        """запрос имени канала"""
        return self.channel['items'][0]['snippet']['title']

    @property
    def video_count(self):
        """запрос количества видео на канале"""
        return self.channel['items'][0]['statistics']['videoCount']

    @property
    def url(self):
        """запрос url"""
        return self.channel['items'][0]['snippet']['thumbnails']["default"]["url"]

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API"""
        return cls.__youtube
