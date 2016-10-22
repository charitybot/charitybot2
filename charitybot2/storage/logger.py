import requests
from charitybot2.storage.logging_service import service_full_url


class LoggingFailedException(Exception):
    pass


class Logger:
    logging_service_url = service_full_url

    def __init__(self, event, source, timeout=0.3):
        self.event = event
        self.source = source
        self.timeout = timeout
        self.validate()

    def validate(self):
        response = requests.get(url=service_full_url + 'health')
        if not response.json()['db']:
            raise LoggingFailedException

    def log(self, level, message):
        payload = {
            'event': self.event,
            'source': self.source,
            'level': level,
            'message': message
        }
        try:
            response = requests.post(url=service_full_url + 'log', json=payload, timeout=self.timeout)
            assert 200 == response.status_code
        except requests.Timeout or requests.ConnectTimeout or requests.ReadTimeout:
            print('Logger timeout!')
            return False
        except Exception:
            raise LoggingFailedException
