from charitybot2.config.event_config import EventConfiguration
from charitybot2.sources.sources import source_names_supported
from tests.tests import TestFilePath

good_source_config_path = TestFilePath().get_config_path('event', 'good_source_event_config.json')
bad_source_config_path = TestFilePath().get_config_path('event', 'bad_source_event_config.json')


class TestEventSourcesValidity:
    def test_invalid_source_url_in_event_config_throws_exception(self):
        ec = EventConfiguration(file_path=bad_source_config_path)
        bad_source_url = ec.get_value('source_url')
        for supported_source_name in source_names_supported:
            assert supported_source_name not in bad_source_url

    def test_valid_source_url_in_event_config_file(self):
        ec = EventConfiguration(file_path=good_source_config_path)
        source_url = ec.get_value('source_url')
        assert 'justgiving' in source_url
