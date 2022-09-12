from asyncio.log import logger
import json
import logging
import os

from lib.utils import SONARCLOUD_URL, SonarPlatform, from_json


class SonarHandler:
    """ Connector with Sonar """

    def __init__(self, attrs) -> None:
        # Unpack configuration
        self._platform = getattr(attrs, 'platform', SonarPlatform.SONARQUBE)
        self.host = getattr(attrs, 'host', None)
        self.port = getattr(attrs, 'port', None)

        project = getattr(attrs, 'project', None)
        self.project = project.pop() if isinstance(project, list) else project

        # Init the logger
        self.logger = logging.getLogger(__name__)

        # Generate the client connetion
        self.client = self.__get_client()

        # Store auth values
        self._autheticated = self.__validate()

    @property
    def autheticated(self):
        """ Getter """
        return self._autheticated.valid

    @autheticated.setter
    def autheticated(self, value):
        if not self._autheticated and value:
            self._autheticated = value

    @property
    def platform(self):
        """ Getter """
        return self._platform

    @platform.setter
    def platform(self, value):
        if not self._platform and value:
            self._platform = value

    @property
    def url(self):
        """ Getter """
        return f"http://{self.host}:{self.port}"

    # Privates
    def __get_client(self):
        module = __import__('sonarqube')

        kargs = dict()
        kargs['token'] = os.getenv('SONAR_TOKEN')
        if self.platform == SonarPlatform.SONARQUBE.value:
            client = 'SonarQubeClient'
            kargs['sonarqube_url'] = self.url if (
                self.host and self.port)else "http://localhost:9000"
        elif self.platform == SonarPlatform.SONARCLOUD.value:
            client = 'SonarCloudClient'
            kargs['sonarcloud_url'] = SONARCLOUD_URL
        else:
            raise TypeError(f'Platform not supported {self.platform}')

        return getattr(module, client)(**kargs)

    # Authentication endpoints
    def __validate(self):
        """ Check credentials. """
        func = 'auth.check_credentials'
        result = self.call(func)
        if result:
            return json.loads(result, object_hook=from_json)

    # Project endpoint
    def search_project(self):
        """ Retrieves a single match for the exact match against project key """
        return_value = None
        func = 'projects.search_projects'

        if not self.project:
            logging.error('No project has been set')
            return return_value

        kargs = dict(projects=self.project)
        projects = self.call(func, **kargs)
        if projects:
            projects = json.dumps(list(projects))
            projects = json.loads(projects, object_hook=from_json)

            match = list(filter(lambda p: p.key == self.project, projects))
            if match:
                return_value = match.pop()

        return return_value

    def create_project(self):
        """ Generate a new project """
        return_value = None
        func = 'projects.create_project'

        if not self.project:
            logger.warning('The Project is not defined')
            return return_value

        kargs = dict(
            project=self.project,
            name=self.project,
            visibility="private"
        )

        result = self.call(func, **kargs)
        if result:
            result = json.dumps(result)
            return_value = json.loads(result, object_hook=from_json)

        return return_value

    def call(self, func, **kargs):
        """ Wrapper functions for client """
        response = None

        base = self.client
        for attr in func.split('.'):
            try:
                base = getattr(base, attr)
                caller = base if callable(base) else None
            except AttributeError:
                logging.warning("Method '%s' not found", attr)

        if caller:
            logging.info(caller.__name__)
            response = caller(**kargs)

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
        return (type, value, traceback)
