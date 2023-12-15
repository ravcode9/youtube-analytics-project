import pytest
import os
from unittest.mock import MagicMock, patch
from src.channel import Channel
from src.api import Api
@pytest.fixture
def mock_youtube_service():
    with patch.object(Api, 'get_youtube_api_key', return_value='your_api_key'):
        youtube_service = MagicMock()
        with patch.object(Channel, 'get_service', return_value=youtube_service):
            yield youtube_service


def test_print_info(capsys, mock_youtube_service):
    channel_id = 'your_channel_id'
    channel = Channel(channel_id)
    channel.print_info()

    captured = capsys.readouterr()
    assert "Title:" in captured.out
    assert "Description:" in captured.out
    assert "URL:" in captured.out
    assert "Subscriber Count:" in captured.out
    assert "Video Count:" in captured.out
    assert "View Count:" in captured.out


def test_to_json(tmpdir, capsys):
    channel_id = 'your_channel_id'
    channel = Channel(channel_id)

    filename = 'test.json'
    json_file_path = os.path.join(str(tmpdir), filename)

    with patch.object(channel, '_fetch_channel_data'):
        # Подменяем вызов _fetch_channel_data, чтобы не обращаться к API
        with patch.object(os.path, 'join', return_value=json_file_path):
            channel.to_json(filename)

    assert os.path.exists(json_file_path)

    captured = capsys.readouterr()
    assert "Произошла ошибка: Нет данных о канале в ответе API" in captured.out


def test_successful_api_response(mock_youtube_service):
    # Modify the mock_youtube_service to return a specific response
    mock_youtube_service.channels().list.return_value.execute.return_value = {
        'items': [{
            'snippet': {
                'title': 'Test Channel',
                'description': 'Test Description'
            },
            'statistics': {
                'subscriberCount': '1000',
                'videoCount': '50',
                'viewCount': '50000'
            }
        }]
    }

    channel_id = 'test_channel_id'
    channel = Channel(channel_id)
    assert channel.title == 'Test Channel'
    assert channel.video_count == 50
    assert channel._subscriber_count == 1000
    assert channel._view_count == 50000