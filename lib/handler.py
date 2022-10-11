""" Sonar Handler """
import json
import logging
import os
from argparse import Namespace

from sonarqube import SonarCloudClient
from sonarqube.utils.exceptions import ValidationError

from lib.utils import SONARCLOUD_URL, SonarPlatform, from_json


class SonarHandler:
    """ Connector with Sonar """

    def __init__(self, attrs: Namespace) -> None:
        # Unpack configuration
        self._platform = getattr(attrs, 'platform', SonarPlatform.SONARQUBE)
        self.host = getattr(attrs, 'host', None)
        self.port = getattr(attrs, 'port', None)

        organization = getattr(attrs, 'organization', None)
        self._organization = organization.pop() if isinstance(
            organization, list) else organization

        # Init the logger
        self.logger = logging.getLogger(__name__)

        # Generate the client connection
        self.client = self.__get_client()

        # Store auth values
        self._authenticated = self.__validate()

    @property
    def authenticated(self):
        """ Getter """
        return self._authenticated.valid

    @property
    def platform(self):
        """ Getter """
        return self._platform

    @property
    def url(self):
        """ Getter """
        return f"http://{self.host}:{self.port}"

    @property
    def organization(self):
        """ Getter """
        return self._organization

    # Privates
    def __get_client(self):
        module = __import__('sonarqube')

        kargs = {
            'token': os.getenv('SONAR_TOKEN')
        }

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
    def list_projects(self):
        """ Retrieves all projects within an organization """
        return_value = None
        func = 'projects.search_projects'

        kargs = {}
        if isinstance(self.client, SonarCloudClient):
            if not self.organization:
                msg = "Organization cannot be empty in Sonar Cloud"
                logging.error(msg)
                raise SonarException(msg)
            kargs['organization'] = self.organization

        projects = self.call(func, **kargs)
        if projects:
            projects = json.dumps(list(projects))
            return_value = json.loads(projects, object_hook=from_json)

        return return_value

    def list_project_branches(self, project_key):
        """ List the branches of a project. """
        return_value = None
        func = 'project_branches.search_project_branches'

        kargs = dict(project=project_key)

        branches = self.call(func, **kargs)
        if branches:
            branches = json.dumps(branches['branches'])
            return_value = json.loads(branches, object_hook=from_json)

        return return_value

    def rename_main_branch(self, project_key, main_branch):
        """ Rename the main branch of a project """
        func = 'project_branches.rename_project_branch'
        kargs = dict(project=project_key, name=main_branch)
        response = self.call(func, **kargs)

        return response

    def call(self, func, **kargs):
        """ Wrapper functions for client """
        caller = None
        response = None

        base = self.client
        for attr in func.split('.'):
            try:
                base = getattr(base, attr)
                caller = base if callable(base) else None
            except AttributeError:
                logging.warning("Method '%s' not found", attr)

        if caller:
            logging.info("%s(%s)", func, kargs)
            response = caller(**kargs)

        return response

    def logout(self):
        """ Logout a user """
        func = 'auth.logout_user'
        return self.call(func)

    def __enter__(self):
        if not self._authenticated:
            self.logger.warning('The Client is not authenticated')
        return self

    def __exit__(self, typ, val, tra):
        self.logout()
        return typ, val, tra


class SonarException(ValidationError):
    """ Sonar Error """
