from lib.handler import SonarHandler
from lib.response import Component

DEFAULT_BRANCH = 'main'


class ProjectBranchCompliant:
    """ Rules for a project branch configuration """
    def __init__(self, project: Component, handler: SonarHandler):
        """ Constructor

        Args:
            project: Sonar Component
            handler: Sonar Connector
        """
        self.project = project
        self.handler = handler
        self.default_branch = DEFAULT_BRANCH

        # Initialize branches
        project_key = self.project.key
        self.branches = self.handler.list_project_branches(project_key)

    @property
    def is_branch_compliant(self) -> bool:
        """ A Project is Branch Compliant when its DEFAULT BRANCH is 'main'

        Args:
            self (Branch): List of Sonar Branch Properties
        """
        return any(b.name == self.default_branch and b.isMain for b in self.branches)

    def set_main_branch(self):
        """ Sets the default branch """
        self.handler.rename_main_branch(self.project.key, self.default_branch)
