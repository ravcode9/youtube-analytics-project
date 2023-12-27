import pytest
from unittest.mock import MagicMock
from src.video import Video

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

def test_fetch_video_data_success(mock_api_key, mock_youtube_service):
    video_id = 'mock_video_id'
    video = Video(video_id)

    mock_youtube_service.videos().list().execute.return_value = {
        'items': [{
            'snippet': {'title': 'Mock Title'},
            'statistics': {'viewCount': '100', 'likeCount': '50'}
        }]
    }

    video._fetch_video_data()

    assert video._title == 'Mock Title'
    assert video._view_count == 100
    assert video._like_count == 50

