import pytest
from charitybot2.charitybot2 import MissingRequiredFileException, CharityBot, create_parser, IllegalArgumentException


class TestParserRequiredArguments:
    parser = create_parser()

    def test_passing_empty_event_name_throws_exception(self):
        args = self.parser.parse_args(['', '--debug'])
        with pytest.raises(IllegalArgumentException):
            CharityBot(args=args)

    def test_passing_non_existent_event_config_throws_exception(self):
        args = self.parser.parse_args(['test', '--debug'])
        with pytest.raises(MissingRequiredFileException):
            CharityBot(args=args)

    def test_passing_existent_event_config(self):
        args = self.parser.parse_args(['config', '--debug'])
        CharityBot(args=args)


class TestParserOptionalArguments:
    parser = create_parser()

    def test_passing_non_existent_twitch_config_in_twitch_mode_throws_exception(self):
        args = self.parser.parse_args(['config', '--debug', '--twitch-config', 'bla'])
        with pytest.raises(MissingRequiredFileException):
            CharityBot(args=args)

    def test_passing_existent_twitch_config_in_twitch_mode(self):
        args = self.parser.parse_args(['config', '--debug', '--twitch-config', 'test_twitch_config'])
        CharityBot(args=args)