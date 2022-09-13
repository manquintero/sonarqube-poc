"""
Proof of Concept for Sonar Interactions
"""
import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys
from argparse import ArgumentError, Namespace

from lib.handler import SonarHandler, SonarException
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
        msg = "Usage of SonarCloud demands an organzation to be provided"
        logging.error(msg)
        raise ArgumentError(None, msg)

    if args.visibility == 'public':
        logging.warning('About to create a public project')


def main():
    """ Entry Point """
    parser = argparse.ArgumentParser(description='Process Sonar Project information')
    parser.add_argument('--platform', dest='platform', action='store', default='sonarqube', choices=SONAR_PLATFORMS)
    parser.add_argument('--project', dest='project', action='store', nargs=1)
    parser.add_argument('--visibility', dest='visibility', action='store', nargs=1, choices=['private', 'public'], default='private')
    parser.add_argument('--organization', dest='organization', action='store', nargs=1)
    args = parser.parse_args()

    # Start Loggers
    setup_logger()

    # Validate inputs
    validate(args)

    with SonarHandler(args) as sonar:
        # Search for project
        if not sonar.autheticated:
            logging.warning('Authentication is not set')
            return

        if not sonar.project:
            logging.warning('The project has not been set')
            return

        project = sonar.search_project()
        if project:
            logging.info("Project '%s' Already Exists", sonar.project)
            return

        logging.info("Project %s not found, creating", sonar.project)

        try:
            sonar_project = sonar.create_project()
            logging.info("Project %s has been generated", sonar.project)
            print(sonar_project)
        except SonarException:
            logging.error("Project not generated")


if __name__ == "__main__":
    main()
