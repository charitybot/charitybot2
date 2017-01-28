import pytest
from charitybot2.configurations import ConfigurationParser, InvalidConfigurationException
from tests.paths_for_tests import valid_config_path, invalid_config_path

valid_test_config_keys = ('key1', 'key2', 'key3')
valid_config_parser = ConfigurationParser(file_path=valid_config_path, keys_required=valid_test_config_keys)


class TestConfigurationParserInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        ('value1', valid_config_parser.get_value(key='key1')),
        ('value2', valid_config_parser.get_value(key='key2')),
        (3, valid_config_parser.get_value(key='key3'))
    ])
    def test_retrieve(self, expected, actual):
        assert expected == actual


class TestConfigurationParserExceptions:
    def test_non_existent_file_throws_exception(self):
        with pytest.raises(FileNotFoundError):
            ConfigurationParser(file_path='c:/blablabla', keys_required=('foo', 'bar'))

    @pytest.mark.parametrize('keys', [
        ('', 'foo'),
        ('foo', ''),
        '',
        None,
        ('', ''),
        ('bla', 'bla')
    ])
    def test_passing_incorrect_keys_throws_exception(self, keys):
        with pytest.raises(InvalidConfigurationException):
            ConfigurationParser(file_path=valid_config_path, keys_required=keys)

    def test_incorrectly_formatted_file_throws_exception(self):
        with pytest.raises(InvalidConfigurationException):
            ConfigurationParser(file_path=invalid_config_path, keys_required=('foo', 'bar'))
