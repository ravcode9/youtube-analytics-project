from datetime import timedelta
import pytest
from unittest.mock import MagicMock, patch
from src.playlist import PlayList


@pytest.fixture
def mock_channel_service(monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr('src.channel.Channel.get_service', MagicMock(return_value=mock_service))
    return mock_service


@pytest.fixture
def mock_youtube_api():
    with patch('src.playlist.Channel.get_service') as mock:
        yield mock


def test_playlist_initialization(mock_channel_service):
    playlist_id = 'mock_playlist_id'
    playlist = PlayList(playlist_id)

    assert playlist._playlist_id == playlist_id
    assert playlist._title is None
    assert playlist._url == f'https://www.youtube.com/playlist?list={playlist_id}'
    assert playlist._videos == []
    assert playlist._playlist_title is None


def test_get_duration():
    playlist = PlayList('mock_playlist_id')
    video_with_duration = MagicMock(duration=timedelta(minutes=2, seconds=30))
    video_without_duration = MagicMock(duration=None)

    assert playlist.get_duration(video_with_duration) == 150.0
    assert playlist.get_duration(video_without_duration) == 0.0


def test_playlist_title(mock_youtube_api):
    playlist_id = '1234'
    mock_youtube_api.return_value.playlists.return_value.list.return_value.execute.return_value = {
        'items': [{'snippet': {'title': 'Test Title'}}]
    }

    playlist = PlayList(playlist_id)

    assert playlist.title == 'Test Title'


def test_show_best_video_no_videos(mock_youtube_api):
    playlist = PlayList('1234')

    assert playlist.show_best_video() is None


def test_total_duration(mock_youtube_api):
    playlist = PlayList('1234')
    video1 = MagicMock(duration=timedelta(minutes=1))
    video2 = MagicMock(duration=timedelta(minutes=2, seconds=30))

    playlist._videos = [video1, video2]

    assert playlist.total_duration == timedelta(minutes=3, seconds=30)
