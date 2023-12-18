from unittest.mock import MagicMock, patch
from src.channel import Channel
from src.api import Api
import pytest

@pytest.fixture
def mock_youtube_service():
    with patch.object(Api, 'get_youtube_api_key', return_value='your_api_key'):
        youtube_service = MagicMock()
        with patch.object(Channel, 'get_service', return_value=youtube_service):
            yield youtube_service

def create_channel(channel_id, subscriber_count):
    channel = Channel(channel_id)
    channel._subscriber_count = subscriber_count
    return channel

def test_str_method():
    channel_id = 'your_channel_id'
    channel = Channel(channel_id)
    expected_str = f"{channel._title} ({channel._url})"
    assert str(channel) == expected_str

def test_add_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 1000)
    channel_2 = create_channel('channel_id_2', 2000)

    result = channel_1 + channel_2
    assert result == 3000

def test_sub_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 2000)
    channel_2 = create_channel('channel_id_2', 1000)

    result = channel_1 - channel_2
    assert result == 1000

def test_eq_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 1500)
    channel_2 = create_channel('channel_id_2', 1500)

    assert channel_1 == channel_2

def test_ne_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 1500)
    channel_2 = create_channel('channel_id_2', 2000)

    assert channel_1 != channel_2

def test_lt_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 1500)
    channel_2 = create_channel('channel_id_2', 2000)

    assert channel_1 < channel_2

def test_le_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 1500)
    channel_2 = create_channel('channel_id_2', 1500)

    assert channel_1 <= channel_2

def test_gt_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 2000)
    channel_2 = create_channel('channel_id_2', 1500)

    assert channel_1 > channel_2

def test_ge_method(mock_youtube_service):
    channel_1 = create_channel('channel_id_1', 2000)
    channel_2 = create_channel('channel_id_2', 2000)

    assert channel_1 >= channel_2
