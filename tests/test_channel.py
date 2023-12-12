import json
import os
from googleapiclient.discovery import Resource
from src.channel import Channel  # Замените 'your_module_name' на имя вашего модуля
import pytest


@pytest.fixture
def channel_instance():
    return Channel("test_channel_id")


def test_channel_print_info(capfd, channel_instance, monkeypatch):
    # Меняем значение переменной окружения API_YOUTUBE для теста
    monkeypatch.setenv('API_YOUTUBE', 'test_api_key')

    # Меняем behavior youtube.channels().list для теста
    class ChannelsList:
        def list(self, **kwargs):
            assert kwargs == {'part': 'snippet,contentDetails,statistics', 'id': 'test_channel_id'}
            return self

        def execute(self):
            return {'kind': 'youtube#channelListResponse', 'etag': 'RuuXzTIr0OoDqI4S0RU6n4FqKEM',
                    'pageInfo': {'totalResults': 0, 'resultsPerPage': 5}}

    channel_instance.youtube.channels().list = ChannelsList()

    # Запускаем метод print_info()
    channel_instance.print_info()

    # Получаем вывод метода print_info()
    captured = capfd.readouterr()

    # Проверяем, что вывод содержит правильные данные
    expected_output = json.dumps({'kind': 'youtube#channelListResponse', 'etag': 'RuuXzTIr0OoDqI4S0RU6n4FqKEM',
                                  'pageInfo': {'totalResults': 0, 'resultsPerPage': 5}}, indent=2, ensure_ascii=False)
    assert captured.out.strip() == expected_output.strip()
