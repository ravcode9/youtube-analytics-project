import pytest
from unittest.mock import MagicMock, patch, Mock
from src.video import Video, PLVideo
from datetime import timedelta
from googleapiclient.errors import HttpError


@pytest.fixture
def mock_api_key(monkeypatch):
    mock_key = 'your_mock_api_key'
    monkeypatch.setattr('src.api.Api.get_youtube_api_key', lambda: mock_key)
    return mock_key

@pytest.fixture
def mock_youtube_service(mock_api_key, monkeypatch):
    mock_service = MagicMock()
    monkeypatch.setattr('src.video.build', MagicMock(return_value=mock_service))
    return mock_service

def test_fetch_video_duration_no_items(mock_api_key, mock_youtube_service):
    video_id = 'mock_video_id'
    plvideo = PLVideo(video_id, 'playlist_id', 300)
    mock_youtube_service.videos().list().execute.return_value = {}

    duration = plvideo._fetch_video_duration()

    assert duration == timedelta()

def test_video_initialization(mock_api_key, mock_youtube_service):
    video_id = 'mock_video_id'
    mock_youtube_service.videos().list().execute.return_value = {
        'items': [{'snippet': {'title': 'Mock Video Title'},
                   'statistics': {'viewCount': 50, 'likeCount': 5}}]
    }
    video = Video(video_id)

    assert video._video_id == video_id
    assert video._title == 'Mock Video Title'
    assert video._url == f'https://www.youtube.com/watch?v={video_id}'
    assert video._view_count == 50
    assert video._like_count == 5


def test_video_initialization_with_api_error(mock_api_key, mock_youtube_service):
    video_id = 'mock_video_id'

    mock_youtube_service.videos().list().execute.return_value = {
        'items': [{
            'snippet': {'title': 'Default Title'},
            'statistics': {'viewCount': 0, 'likeCount': 0}
        }]
    }

    video = Video(video_id)

    assert video._video_id == video_id
    assert video._title == 'Default Title'
    assert video._url == f'https://www.youtube.com/watch?v={video_id}'
    assert video._view_count == 0
    assert video._like_count == 0


def test_parse_duration_method(mock_api_key, mock_youtube_service):
    video_id = 'mock_video_id'
    playlist_id = 'mock_playlist_id'
    duration = 300
    mock_youtube_service.videos().list().execute.return_value = {}
    plvideo = PLVideo(video_id, playlist_id, duration)
    result = plvideo._fetch_video_duration()
    assert result == timedelta()

@patch('src.video.build')
def test_video_title(mock_build):
    video_id = '1234'
    mock_build.return_value.videos.return_value.list.return_value.execute.return_value = {
        'items': [{'snippet': {'title': 'Video Title'},
                'statistics': {'viewCount': 100, 'likeCount': 10}}]}

    video = Video(video_id)

    assert video.title == 'Video Title'
    assert video.view_count == 100
    assert video.like_count == 10


@patch('src.video.build')
def test_plvideo_fetch_video_duration_api_error(mock_build):
    video_id = 'mock_video_id'
    playlist_id = 'mock_playlist_id'
    duration = 300
    mock_build.return_value.videos.return_value.list.return_value.execute.side_effect = HttpError(Mock(), b'Error content')

    plvideo = PLVideo(video_id, playlist_id, duration)
    result = plvideo._fetch_video_duration()
    assert result == timedelta()