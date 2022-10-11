""" Test Cases for utils.py """
import unittest

from lib.response import Validate, Component, Branch
from lib.utils import from_json

VALID_PAYLOAD = {'valid': True}
COMPONENT_PAYLOAD = {
    'organization': 'my-org',
    'key': 'my-org_project',
    'name': 'project',
    'qualifier': 'TRK',
    'visibility': 'private',
    'lastAnalysisDate': '2022-10-10T22:31:50+0200',
    'revision': 'c658d235b686d8e5b67d7991006ff8f874cb8e7e'
}
BRANCH_PAYLOAD = {
    'name': 'main',
    'isMain': True,
    'type': 'LONG',
    'status': {
        'bugs': 0,
        'vulnerabilities': 0,
        'codeSmells': 0
    },
    'analysisDate': '2022-10-10T22:31:50+0200',
    'commit': {
        'sha': 'c658d235b686d8e5b67d7991006ff8f874cb8e7e',
        'author': {
            'name': 'Name', 'login': 'name@github', 'avatar': 'fb1a30fc483b5001f294c686f70d460c'
        },
        'date': '2022-10-10T20:51:08+0200',
        'message': 'build: Add Pylint pre-commit'
    }
}


class TestFromJson(unittest.TestCase):
    """ Test Case for from_jsom """

    def test_from_json(self):
        """ Test Case for Default Types """
        payload = {}
        value = from_json(payload)
        self.assertIsInstance(value, dict)

    def test_from_json_validate(self):
        """ Test Case for Validate Types """
        value = from_json(VALID_PAYLOAD)
        self.assertIsInstance(value, Validate)

    def test_from_json_component(self):
        """ Test Case for Component Types """
        value = from_json(COMPONENT_PAYLOAD)
        self.assertIsInstance(value, Component)

    def test_from_json_branch(self):
        """ Test Case for Branch Types """
        payload = BRANCH_PAYLOAD
        value = from_json(payload)
        self.assertIsInstance(value, Branch)

    def test_from_json_str(self):
        """ Test Case for str representation  """
        value = from_json(VALID_PAYLOAD)
        self.assertIsInstance(str(value), str)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
