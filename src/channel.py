import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.api import Api

class Channel:
    def __init__(self, channel_id):
        self._channel_id = channel_id
        self._title = None
        self._description = None
        self._url = None
        self._subscriber_count = None
        self._video_count = None
        self._view_count = None
        self._fetch_channel_data()

    def __str__(self):
        return f"{self._title} ({self._url})"

    def __add__(self, other):
        return self._subscriber_count + other._subscriber_count

    def __sub__(self, other):
        return self._subscriber_count - other._subscriber_count

    def __eq__(self, other):
        return self._subscriber_count == other._subscriber_count

    def __ne__(self, other):
        return self._subscriber_count != other._subscriber_count

    def __lt__(self, other):
        return self._subscriber_count < other._subscriber_count

    def __le__(self, other):
        return self._subscriber_count <= other._subscriber_count

    def __gt__(self, other):
        return self._subscriber_count > other._subscriber_count

    def __ge__(self, other):
        return self._subscriber_count >= other._subscriber_count


    def _fetch_channel_data(self):
        try:
            self._title = "Default Title"
            self._description = "Default Description"
            self._url = f'https://www.youtube.com/channel/{self._channel_id}'
            self._subscriber_count = 0
            self._video_count = 0
            self._view_count = 0

            # Использование YouTube API для получения данных о канале
            youtube = Channel.get_service()
            response = youtube.channels().list(
                part='snippet,statistics',
                id=self._channel_id
            ).execute()

            if 'items' in response:
                # Извлечение актуальной информации из ответа API
                channel = response['items'][0]
                snippet = channel['snippet']
                statistics = channel['statistics']

                # Заполнение атрибутов экземпляра
                self._title = snippet['title']
                self._description = snippet['description']
                self._url = f'https://www.youtube.com/channel/{self._channel_id}'
                self._subscriber_count = int(statistics['subscriberCount'])
                self._video_count = int(statistics['videoCount'])
                self._view_count = int(statistics['viewCount'])
            else:
                print(f'Произошла ошибка: Нет данных о канале в ответе API')

        except HttpError as e:
            print(f'Произошла ошибка: {e}')

    def print_info(self):
        """Печатает информацию о канале в удобочитаемом формате"""
        print(f"Title: {self._title}")
        print(f"Description: {self._description}")
        print(f"URL: {self._url}")
        print(f"Subscriber Count: {self._subscriber_count}")
        print(f"Video Count: {self._video_count}")
        print(f"View Count: {self._view_count}")

    def _create_youtube_api(self):
        """Создает объект API YouTube с использованием ключа из конфига."""
        api_key = Api.get_youtube_api_key()
        return build('youtube', 'v3', developerKey=api_key)

    @property
    def title(self):
        return self._title

    @property
    def video_count(self):
        return self._video_count

    @property
    def url(self):
        return self._url

    @classmethod
    def get_service(cls):
        api_key = Api.get_youtube_api_key()
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, filename):
        # Получение абсолютного пути к файлу внутри пакета src
        json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

        # Сохранение данных о канале в JSON-файл внутри пакета src
        data = {
            'id': self._channel_id,
            'title': self._title,
            'description': self._description,
            'url': self._url,
            'subscriber_count': self._subscriber_count,
            'video_count': self._video_count,
            'view_count': self._view_count
        }
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file)