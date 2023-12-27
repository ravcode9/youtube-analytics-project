from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.api import Api

class Video:
    def __init__(self, video_id):
        self._video_id = video_id
        self._title = "Default Title"
        self._url = f'https://www.youtube.com/watch?v={self._video_id}'
        self._view_count = 0
        self._like_count = 0
        self._fetch_video_data()

    def __str__(self):
        return self._title

    def _fetch_video_data(self):
        """
        Получает данные о видео с использованием YouTube API.
        Обновляет атрибуты объекта на основе полученных данных.
        """
        try:
            youtube = self.get_service()
            response = youtube.videos().list(
                part='snippet,statistics',
                id=self._video_id
            ).execute()

            if 'items' in response:
                video = response['items'][0]
                snippet = video['snippet']
                statistics = video['statistics']

                self._title = snippet['title']
                self._view_count = int(statistics.get('viewCount', 0))
                self._like_count = int(statistics.get('likeCount', 0))
            else:
                print(f'Произошла ошибка: Нет данных о видео в ответе API')

        except HttpError as e:
            print(f'Произошла ошибка: {e}')

    @classmethod
    def get_service(cls):
        api_key = Api.get_youtube_api_key()
        return build('youtube', 'v3', developerKey=api_key)

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self._playlist_id = playlist_id

    def __str__(self):
        return super().__str__()
