import datetime
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

    @property
    def title(self):
        return self._title

    @property
    def view_count(self):
        return self._view_count

    @property
    def like_count(self):
        return self._like_count

    def _fetch_video_data(self):
        try:
            youtube = self.get_service()
            response = youtube.videos().list(
                part='snippet,statistics',
                id=self._video_id
            ).execute()

            if 'items' in response and response['items']:
                video = response['items'][0]
                snippet = video['snippet']
                statistics = video['statistics']

                self._title = snippet['title']
                self._view_count = int(statistics.get('viewCount', 0))
                self._like_count = int(statistics.get('likeCount', 0))
            else:
                print(f'Произошла ошибка: Нет данных о видео в ответе API')
                self._title = None
                self._view_count = None
                self._like_count = None

        except HttpError as e:
            print(f'Произошла ошибка: {e}')
            self._title = None
            self._view_count = None
            self._like_count = None

    @classmethod
    def get_service(cls):
        api_key = Api.get_youtube_api_key()
        return build('youtube', 'v3', developerKey=api_key)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id, duration=None):
        self._duration = duration
        super().__init__(video_id)
        self._playlist_id = playlist_id
        self._fetch_video_data()

    @property
    def duration(self):
        return self._duration

    def _fetch_video_data(self):
        if self._duration is None:
            self._duration = self._fetch_video_duration()

        super()._fetch_video_data()

    def _fetch_video_duration(self):
        try:
            youtube = self.get_service()
            response = youtube.videos().list(
                part='contentDetails',
                id=self._video_id
            ).execute()

            if 'items' in response:
                video_details = response['items'][0]['contentDetails']
                duration_iso = video_details['duration']
                return self._parse_duration(duration_iso)

        except HttpError as e:
            print(f'Произошла ошибка при получении данных о видео: {e}')

        return datetime.timedelta()

    @staticmethod
    def _parse_duration(duration_iso):
        duration_str = duration_iso[2:]
        duration = datetime.timedelta()

        if 'H' in duration_str:
            hours, duration_str = duration_str.split('H')
            duration += datetime.timedelta(hours=int(hours))

        if 'M' in duration_str:
            minutes, duration_str = duration_str.split('M')
            duration += datetime.timedelta(minutes=int(minutes))

        if 'S' in duration_str:
            seconds, _ = duration_str.split('S')
            duration += datetime.timedelta(seconds=int(seconds))

        return duration