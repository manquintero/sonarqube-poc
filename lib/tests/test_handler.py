""" Test Cases for handler.py """
import json
import unittest
from argparse import Namespace
from unittest.mock import patch

from sonarqube import SonarQubeClient, SonarCloudClient
from sonarqube.cloud import SonarCloudProjects
from sonarqube.community import SonarQubeAuth, SonarQubeProjectBranches

from lib.handler import SonarHandler, SonarException
from lib.response import Branch, Component
from lib.rules import DEFAULT_BRANCH
from lib.tests.test_utils import VALID_PAYLOAD, COMPONENT_PAYLOAD, BRANCH_PAYLOAD


class SonarHandlerTestCase(unittest.TestCase):
    """ Test cases for SonarHandler """

    def setUp(self) -> None:
        """ Locals """
        self.project_key = 'my-org_project'
        self.cloud_settings = Namespace(platform='sonarcloud', organization="my-org")

    def test_default_constructor(self):
        """ Default constructor needs attributes """
        with self.assertRaises(TypeError):
            SonarHandler(None)

    def test_invalid_client(self):
        """ Verify an invalid sonar client """
        with self.assertRaises(TypeError):
            SonarHandler(Namespace(platform='invalid'))

    @patch.object(SonarQubeAuth, 'check_credentials')
    def test_sonar_client_authenticated(self, check_credentials_mock):
        """ Verify a client is Authenticated via a Valid Payload hit """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)

        test_cases = {
            'sonarqube': SonarQubeClient,
            'sonarcloud': SonarCloudClient,
        }

        for key, expected in test_cases.items():
            with self.subTest(key):
                attrs = Namespace(platform=key)
                handler = SonarHandler(attrs)
                self.assertIsInstance(handler.client, expected)
                self.assertTrue(handler.authenticated)

    @patch.object(SonarQubeAuth, 'check_credentials')
    @patch.object(SonarQubeAuth, 'logout_user')
    def test_context_manger(self, check_credentials_mock, logout_user_mock):
        """ Verify the logout call in a Context Manager exit """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)
        logout_user_mock.return_value = ''
        attrs = Namespace(platform='sonarcloud')
        with SonarHandler(attrs):
            pass
        self.assertTrue(logout_user_mock.called)

    @patch.object(SonarQubeAuth, 'check_credentials')
    def test_invalid_call(self, check_credentials_mock):
        """ An invalid call should return and empty response """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)

        attrs = Namespace(platform='sonarcloud')
        handler = SonarHandler(attrs)
        self.assertIsNone(handler.call('unknown'))

    @patch.object(SonarQubeAuth, 'check_credentials')
    def test_url(self, check_credentials_mock):
        """ Test custom url """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)

        host = "awesome"
        port = 1234
        attrs = Namespace(platform='sonarcloud', host=host, port=port)
        handler = SonarHandler(attrs)

        expected = f"http://{host}:{port}"
        self.assertEqual(handler.url, expected)

    @patch.object(SonarQubeAuth, 'check_credentials')
    def test_list_projects_no_organization(self, check_credentials_mock):
        """ Test List Projects call """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)

        attrs = Namespace(platform='sonarcloud')
        handler = SonarHandler(attrs)
        with self.assertRaises(SonarException):
            handler.list_projects()

    @patch.object(SonarQubeAuth, 'check_credentials')
    @patch.object(SonarCloudProjects, 'search_projects')
    def test_list_projects_(self, search_projects_mock, check_credentials_mock):
        """ Test List Projects call """
        items = 2
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)
        # Generator of Projects
        search_projects_mock.return_value = (COMPONENT_PAYLOAD for _ in range(items))

        handler = SonarHandler(self.cloud_settings)
        projects = handler.list_projects()
        # Verify the result is a list of 2 Component objects
        self.assertIsInstance(projects, list)
        self.assertEqual(items, len(projects))
        self.assertTrue(all(isinstance(p, Component) for p in projects))

    @patch.object(SonarQubeAuth, 'check_credentials')
    @patch.object(SonarQubeProjectBranches, 'search_project_branches')
    def test_list_project_branches(self, search_project_branches_mock, check_credentials_mock):
        """ Test calls to list_project_branches """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)
        search_project_branches_mock.return_value = {'branches': [BRANCH_PAYLOAD]}

        handler = SonarHandler(self.cloud_settings)
        branches = handler.list_project_branches(self.project_key)

        # Verify is a List compromised of 1 Branch Element
        self.assertIsInstance(branches, list)
        self.assertEqual(1, len(branches))
        self.assertTrue(all(isinstance(b, Branch) for b in branches))

    @patch.object(SonarQubeAuth, 'check_credentials')
    @patch.object(SonarQubeProjectBranches, 'delete_project_branch')
    def test_delete_branch(self, search_project_branches_mock, check_credentials_mock):
        """ Test calls to delete_branch """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)
        search_project_branches_mock.return_value = b''

        handler = SonarHandler(self.cloud_settings)
        response = handler.delete_branch(self.project_key, DEFAULT_BRANCH)

        # Verify an empty response is generated
        self.assertEqual(b'', response)

    @patch.object(SonarQubeAuth, 'check_credentials')
    @patch.object(SonarQubeProjectBranches, 'rename_project_branch')
    def test_rename_main_branch(self, search_project_branches_mock, check_credentials_mock):
        """ Test calls to rename_main_branch """
        check_credentials_mock.return_value = json.dumps(VALID_PAYLOAD)
        search_project_branches_mock.return_value = b''

        handler = SonarHandler(self.cloud_settings)
        response = handler.rename_main_branch(self.project_key, DEFAULT_BRANCH)

        # Verify an empty response is generated
        self.assertEqual(b'', response)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
