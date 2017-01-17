import time

from charitybot2.events.currency import Currency


class InvalidArgumentException(Exception):
    pass


class Donation:
    def __init__(self, old_amount, new_amount, timestamp=None, rounding=2, notes='', valid=True):
        self.rounding = rounding
        self.timestamp = int(time.time()) if timestamp is None else timestamp
        self.old_amount = self.parse_donation_input(old_amount)
        self.new_amount = self.parse_donation_input(new_amount)
        self.notes = notes
        self.valid = valid
        self.validate_resultant_amounts()
        self.donation_amount = self.new_amount - self.old_amount

    def __str__(self):
        return 'Donation of {} at {} with notes: {} and validity: {}'.format(
            self.get_donation_amount(),
            self.get_timestamp(),
            self.get_notes(),
            self.get_validity())

    def parse_donation_input(self, amount):
        if amount == '':
            raise InvalidArgumentException
        if isinstance(amount, str):
            amount = amount.replace(',', '')
            for symbol in Currency.symbols:
                amount = amount.replace(symbol, '')
        return round(float(amount), self.rounding)

    def validate_resultant_amounts(self):
        if self.new_amount < self.old_amount and self.valid:
            raise InvalidArgumentException

    def get_donation_amount(self):
        return round(self.donation_amount, self.rounding)

    def get_total_raised(self):
        return round(self.new_amount, self.rounding)

    def get_timestamp(self):
        return int(self.timestamp)

    def get_notes(self):
        return self.notes

    def get_validity(self):
        return self.valid if isinstance(self.valid, bool) else self.valid == 1
