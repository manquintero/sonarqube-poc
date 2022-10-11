"""
Sonar CLI helper
"""
import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys
from argparse import ArgumentError, Namespace

from lib.handler import SonarHandler, SonarException
from lib.rules import ProjectBranchCompliant
from lib.utils import SonarPlatform

SONAR_PLATFORMS = list(p.value for p in SonarPlatform)


def setup_logger():
    """ Install logger for main and libraries """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Add log file
    logger.addHandler(RotatingFileHandler(
        'master.log', maxBytes=2000000, backupCount=10))

    # Add stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def validate(args: Namespace):
    """ Inputs Rules """
    # Whenever sonarcloud is enabled an organization is mandatory
    if args.platform == SonarPlatform.SONARCLOUD.value and not args.organization:
        msg = "Usage of SonarCloud demands an organization to be provided"
        logging.error(msg)
        raise ArgumentError(None, msg)


def main():
    """ Entry Point """
    parser = argparse.ArgumentParser(description='Process Sonar Project information')
    parser.add_argument('--platform', dest='platform', action='store', default='sonarcloud', choices=SONAR_PLATFORMS)
    parser.add_argument('--organization', dest='organization', action='store', nargs=1)
    args = parser.parse_args()

    # Start Loggers
    setup_logger()

    # Validate inputs
    validate(args)

    with SonarHandler(args) as sonar:
        # Search for project
        if not sonar.authenticated:
            logging.warning('Authentication is not set')
            return

        try:
            projects = sonar.list_projects()
        except SonarException:
            logging.error("Unable to calculate Projects in %s", sonar.organization)

        if not projects:
            logging.error("No projects where found for %s organization", sonar.organization)
            return

        # Calculate non-compliant projects
        branch_audit_projects = [ProjectBranchCompliant(project, sonar) for project in projects]
        for deviated in filter(lambda p: not p.is_branch_compliant, branch_audit_projects):
            project_key = deviated.project.key
            logging.info('Project %s is not compliant, modifying settings', project_key)
            try:
                deviated.set_main_branch()
            except SonarException:
                logging.error('Unable to set main branch for %s', project_key)


if __name__ == "__main__":
    main()
