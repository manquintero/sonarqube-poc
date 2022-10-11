""" Test Cases for rules.py """
import unittest
from unittest.mock import create_autospec

from lib.handler import SonarHandler
from lib.response import Component, Branch
from lib.rules import ProjectBranchCompliant
from lib.tests.test_utils import COMPONENT_PAYLOAD, BRANCH_PAYLOAD


class ProjectBranchCompliantTestCase(unittest.TestCase):
    """ Test Cases for ProjectBranchCompliant"""

    def setUp(self) -> None:
        self.project = Component(COMPONENT_PAYLOAD)
        self.handler = create_autospec(SonarHandler)
        self.handler.list_project_branches.return_value = [
            Branch(BRANCH_PAYLOAD)
        ]

    def test_empty_constructor(self):
        """ Verify empty constructor fails """
        with self.assertRaises(TypeError):
            # pylint: disable=no-value-for-parameter
            ProjectBranchCompliant()

    def test_project_branch_compliant(self):
        """ Verify a valid project """
        branch = ProjectBranchCompliant(self.project, self.handler)
        self.assertTrue(branch.is_branch_compliant)

    def test_set_main_branch(self):
        """ Verify rename_main_branch is called """
        branch = ProjectBranchCompliant(self.project, self.handler)
        branch.set_main_branch()
        self.assertTrue(self.handler.rename_main_branch.called)

    def test_set_main_branch_already_exists(self):
        """ Verify a non-main branch is delete before renaming is called """
        self.handler.list_project_branches.return_value = [
            Branch(dict(name='master', isMain=True)),
            Branch(dict(name='main', isMain=False))
        ]
        branch = ProjectBranchCompliant(self.project, self.handler)
        branch.set_main_branch()

        self.assertTrue(self.handler.delete_branch.called)
        self.assertTrue(self.handler.rename_main_branch.called)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
