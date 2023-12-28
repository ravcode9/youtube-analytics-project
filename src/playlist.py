import datetime
from googleapiclient.errors import HttpError
from src.video import PLVideo
from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self._title = None
        self._url = f'https://www.youtube.com/playlist?list={self._playlist_id}'
        self._videos = []
        self._playlist_title = None
        self._fetch_playlist_data()


    @property
    def title(self):
        if not self._title:
            self._fetch_playlist_data()
        return self._title


    @property
    def url(self):
        return self._url

    @property
    def total_duration(self):
        if not self._videos:
            self._fetch_playlist_data()
        total_seconds = sum(self.get_duration(video) for video in self._videos)
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        if not self._videos:
            self._fetch_playlist_data()
        if not self._videos:
            return None

        best_video = max(self._videos, key=lambda video: video._like_count)
        video_url = best_video._url

        video_id_index = video_url.find('?v=')
        if video_id_index != -1:
            video_id = video_url[video_id_index + 3:]
            video_url = f"https://youtu.be/{video_id}"

        return video_url

    @property
    def playlist_title(self):
        if not self._playlist_title:
            self._fetch_playlist_data()
        return self._playlist_title

    def get_duration(self, video):
        if hasattr(video, 'duration'):
            return video.duration.total_seconds() if video.duration else 0
        else:
            return 0

    def _fetch_playlist_data(self):
        try:
            youtube = Channel.get_service()

            # Получаем данные о плейлисте
            playlist_response = youtube.playlists().list(
                part='snippet',
                id=self._playlist_id
            ).execute()

            if 'items' in playlist_response and playlist_response['items']:
                playlist = playlist_response['items'][0]['snippet']
                self._title = playlist['title']
                self._playlist_title = playlist['title']

                # Получаем список видео в плейлисте
                playlist_items_response = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=self._playlist_id,
                    maxResults=50
                ).execute()

                video_ids = [item['contentDetails']['videoId'] for item in playlist_items_response['items']]

                # Получаем данные о каждом видео
                for video_id in video_ids:
                    duration = self._fetch_video_duration(youtube, video_id)
                    video = PLVideo(video_id, self._playlist_id, duration)
                    self._videos.append(video)

        except HttpError as e:
            print(f'Произошла ошибка при получении данных о плейлисте: {e}')

    def _fetch_video_duration(self, youtube, video_id):
        try:
            response = youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()

            if 'items' in response:
                video_details = response['items'][0]['contentDetails']
                duration_iso = video_details['duration']
                return PLVideo._parse_duration(duration_iso)

        except HttpError as e:
            print(f'Произошла ошибка при получении данных о видео: {e}')

        return datetime.timedelta()

