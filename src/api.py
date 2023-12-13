import os

class Api:
    @staticmethod
    def get_youtube_api_key():
        return os.getenv('API_YOUTUBE')
