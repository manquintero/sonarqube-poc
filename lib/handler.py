""" Sonar Handler """
import json
import logging
import os
import re
from sonarqube import SonarCloudClient
from sonarqube.utils.exceptions import ValidationError

from lib.utils import SONARCLOUD_URL, SonarPlatform, from_json


class SonarHandler:
    """ Connector with Sonar """

    def __init__(self, attrs) -> None:
        # Unpack configuration
        self._platform = getattr(attrs, 'platform', SonarPlatform.SONARQUBE)
        self.host = getattr(attrs, 'host', None)
        self.port = getattr(attrs, 'port', None)

        organization = getattr(attrs, 'organization', None)
        self._organization = organization.pop() if isinstance(
            organization, list) else organization

        # Normalize the project Key
        project = getattr(attrs, 'project', None)
        if isinstance(project, list):
            project = project.pop()
        self.project = project

        self._visibility = getattr(attrs, 'visibility', 'private')

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
        """ Setter """
        if not self._platform and value:
            self._platform = value

    @property
    def url(self):
        """ Getter """
        return f"http://{self.host}:{self.port}"

    @property
    def organization(self):
        """ Getter """
        return self._organization

    @organization.setter
    def organization(self, value):
        """ Setter """
        if not self._organization and value:
            self._organization = value

    @property
    def visibility(self):
        """ Getter """
        return self._visibility

    # Privates
    def __get_client(self):
        module = __import__('sonarqube')

        kargs = dict()
        kargs['token'] = os.getenv('SONAR_TOKEN')

        if self.platform == SonarPlatform.SONARQUBE.value:
            client = 'SonarQubeClient'
            kargs['sonarqube_url'] = self.url if (
                self.host and self.port) else "http://localhost:9000"
        elif self.platform == SonarPlatform.SONARCLOUD.value:
            client = 'SonarCloudClient'
            kargs['sonarcloud_url'] = SONARCLOUD_URL
        else:
            raise TypeError(f'Platform not supported {self.platform}')

        return getattr(module, client)(**kargs)

    # Authentication endpoints
    def __validate(self):
        """ Check credentials. """
        return_value = None
        func = 'auth.check_credentials'
        result = self.call(func)
        if result:
            return_value = json.loads(result, object_hook=from_json)

        return return_value

    # Project endpoint
    def search_project(self):
        """ Retrieves a single match for the exact match against project key """
        return_value = None
        func = 'projects.search_projects'

        if not self.project:
            logging.error('No project has been set')
            return return_value

        kargs = dict()

        if isinstance(self.client, SonarCloudClient):
            kargs['organization'] = self.organization

            # If organization is defined, it needs to be prefixed to the project name
            pattern = re.compile(f'^{self._organization}_{self.project}$')
            kargs['project'] = self.project if pattern.match(
                self.project) else f'{self.organization}_{self.project}'
        else:
            kargs['project'] = self.project

        projects = self.call(func, **kargs)
        if projects:
            projects = json.dumps(list(projects))
            projects = json.loads(projects, object_hook=from_json)

            match = list(filter(lambda p: p.key == kargs['project'], projects))
            if match:
                return_value = match.pop()

        return return_value

    def create_project(self):
        """ Generate a new project """
        return_value = None
        func = 'projects.create_project'

        if not self.project:
            self.logger.warning('The Project is not defined')
            return return_value

        kargs = dict(
            project=self.project,
            name=self.project,
            visibility=self.visibility
        )

        if isinstance(self.client, SonarCloudClient):
            kargs['organization'] = self.organization

        try:
            result = self.call(func, **kargs)
            if result:
                result = json.dumps(result)
                return_value = json.loads(result, object_hook=from_json)
        except ValidationError as validation_error:
            msg = str(validation_error)
            if re.search('Could not create Project, key already exists:', msg):
                logging.warning(msg)
                exception = validation_error

            # Raise Unhandled exceptions
            if exception:
                raise SonarException from validation_error

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
            logging.info("%s(%s)", caller.__name__, kargs)
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


class SonarException(ValidationError):
    """ Sonar Error """
