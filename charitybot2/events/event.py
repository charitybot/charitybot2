from charitybot2.events.currency import Currency
from charitybot2.storage.repository import Repository


class EventInvalidException(Exception):
    pass


class EventAlreadyFinishedException(Exception):
    pass


class Event:
    def __init__(self, event_configuration, db_path):
        self.event_configuration = event_configuration
        self.name = event_configuration.get_internal_name()
        self.repository = Repository(db_path=db_path, debug=True)
        self.amount_raised = 0

    def update_event(self, event_configuration):
        if self.event_already_registered():
            self.repository.update_event(event_configuration=event_configuration)
            self.event_configuration = self.repository.get_event_configuration(
                event_name=self.event_configuration.get_internal_name())

    def register_event(self, starting_amount=0):
        if not self.event_already_registered():
            self.repository.register_event(
                event_configuration=self.event_configuration,
                starting_amount=starting_amount)

    def event_already_registered(self):
        return self.repository.event_exists(event_name=self.event_configuration.get_internal_name())

    def get_configuration(self):
        return self.event_configuration

    def get_amount_raised(self):
        return self.amount_raised

    def set_amount_raised(self, amount):
        self.amount_raised = amount

    def increment_amount_raised(self, amount_increase):
        self.amount_raised += amount_increase

    def get_starting_amount(self):
        return self.repository.get_starting_amount(event_name=self.event_configuration.get_internal_name())
