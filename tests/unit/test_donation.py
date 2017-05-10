import json

import pytest
import time
from charitybot2.models.donation import Donation, InvalidDonationException

test_donation = Donation(
    amount=50,
    event_identifier='event_identifier',
    timestamp=999999,
    identifier='identifier',
    notes='Automated')


class TestDonationInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        (50, test_donation.amount),
        (999999, test_donation.timestamp),
        ('identifier', test_donation.identifier),
        ('event_identifier', test_donation.event_identifier),
        ('Automated', test_donation.notes),
        (True, test_donation.validity)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual

    @pytest.mark.parametrize('amount', [
        '12345.67',
        '12,345.67',
        '1234,5.67',
        '1,2345.67'
    ])
    def test_passing_amount_string_with_commas_parses_properly(self, amount):
        donation = Donation(amount=amount, event_identifier='event')
        assert 12345.67 == donation.amount

    @pytest.mark.parametrize('amount', [
        123.45,
        123.454,
        123.4543,
        123.45432
    ])
    def test_donation_amount_rounding(self, amount):
        donation = Donation(amount=amount, event_identifier='event')
        assert 123.45 == donation.amount

    def test_donation_optional_defaults(self):
        donation = Donation(amount=1, event_identifier='event')
        assert int(time.time()) + 2 >= donation.timestamp >= int(time.time()) - 2
        assert None is donation.identifier
        assert None is donation.notes
        assert True is donation.validity


class TestDonationExceptions:
    @pytest.mark.parametrize('amount,timestamp,event_identifier,identifier', [
        (0, 0, 'event', 'bla'),
        (1, 0, None, 'bla'),
        (50, -20, None, None),
        ('', 0, None, None),
        ('foobar', 0, None, None)
    ])
    def test_incorrect_values_throws_exception(self, amount, timestamp, event_identifier, identifier):
        with pytest.raises(InvalidDonationException):
            Donation(
                amount=amount,
                event_identifier=event_identifier,
                timestamp=timestamp,
                identifier=identifier)


class TestDonationMethods:
    test_donation_dict = dict(
        amount=test_donation.amount,
        event_identifier=test_donation.event_identifier,
        timestamp=test_donation.timestamp,
        identifier=test_donation.identifier,
        notes=test_donation.notes,
        valid=test_donation.validity)

    def test_conversion_from_valid_dict(self):
        donation = Donation.from_dict(self.test_donation_dict)
        assert test_donation.amount == donation.amount
        assert test_donation.event_identifier == donation.event_identifier
        assert test_donation.timestamp == donation.timestamp
        assert test_donation.identifier == donation.identifier
        assert test_donation.notes == donation.notes
        assert test_donation.validity == donation.validity

    @pytest.mark.parametrize('donation_dict', [
        dict(),
        dict(foo='bar'),
        dict(amount='-3945'),
        dict(valid=None),
        None,
        1,
        2.0,
        object,
        ''
    ])
    def test_conversion_from_invalid_dict_throws_exception(self, donation_dict):
        with pytest.raises(InvalidDonationException):
            donation = Donation.from_dict(donation_dict=donation_dict)

    def test_conversion_from_valid_json(self):
        donation_json = json.dumps(self.test_donation_dict)
        donation = Donation.from_json(donation_json=donation_json)
        assert test_donation.amount == donation.amount
        assert test_donation.event_identifier == donation.event_identifier
        assert test_donation.timestamp == donation.timestamp
        assert test_donation.identifier == donation.identifier
        assert test_donation.notes == donation.notes
        assert test_donation.validity == donation.validity

    @pytest.mark.parametrize('donation_json', [
        None,
        1,
        1.0,
        object,
        '',
        'bla',
        '{}',
        '[]',
        'foobarr',
        '{"something" : "or other"}',
        '{"amount": 9001}'
    ])
    def test_conversion_from_invalid_json_throws_exception(self, donation_json):
        with pytest.raises(InvalidDonationException):
            donation = Donation.from_json(donation_json=donation_json)

    def test_conversion_to_dict(self):
        assert self.test_donation_dict == test_donation.to_dict()

    def test_conversion_to_json(self):
        test_donation_json = json.dumps(self.test_donation_dict)
        assert test_donation_json == test_donation.to_json()