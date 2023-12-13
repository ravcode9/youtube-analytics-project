import json
from googleapiclient.discovery import build
from src.api import Api

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала и ключом API."""
        self.channel_id = channel_id
        self.api_key = Api.get_youtube_api_key()
        self.youtube = self._create_youtube_api()

    def _create_youtube_api(self):
        """Создает объект API YouTube с использованием ключа из конфига."""
        return build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self) -> None:
        """Печатает информацию о канале в удобочитаемом формате"""
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=self.channel_id
        )

        response = request.execute()

        # Выводим информацию о канале в json-подобном формате
        print(json.dumps(response, indent=2, ensure_ascii=False))