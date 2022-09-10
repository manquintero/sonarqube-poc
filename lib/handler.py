import json
import logging
import os
from sonarqube import SonarQubeClient

from lib.response import from_json


class SonarHandler:

    def __init__(self, project=None) -> None:
        self.host = "localhost"
        self.port = 8080
        self.project = project

        self.url = "http://%s:%d" % (self.host, self.port)
        self.url_api = self.url + '/api'

        # Init the logger
        self.logger = logging.getLogger(__name__)

        # Properties
        sonar_token = os.getenv('SONARQU_TOKEN')
        self.client = SonarQubeClient(self.url, token=sonar_token)

        # Store auth values
        self._autheticated = self.validate()

    @property
    def autheticated(self):
        return self._autheticated

    @autheticated.setter
    def autheticated(self, value):
        if not self._autheticated and value:
            self._autheticated = value

    # Authentitation endpoints
    def validate(self):
        """ Check credentials. """
        func = 'auth.check_credentialss'
        result = self.call(func)
        if result:
            return json.loads(result, object_hook=from_json)

    def call(self, func, *args):
        ''' Wrapper functions for client '''
        response = None

        base = self.client
        for attr in func.split('.'):
            try:
                base = getattr(base, attr)
                caller = base if callable(base) else None
            except AttributeError:
                logging.warning("Method '{}' not found".format(attr))

        if caller:
            logging.info(caller.__name__)
            response = caller(*args)

        return response

    def logout(self):
        """ Logout a user """
        func = 'auth.logout_user'
        return self.call(func)

    def __enter__(self):
        if not self._autheticated:
            self.logger.warning('The Client is not authenticated')
        return self

    def __exit__(self, type, value, traceback):
        self.logout()