"""
Proof of Concept for Sonar Interactions
"""
import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys

from lib.handler import SonarHandler


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


def main():
    """ Entry Point """
    parser = argparse.ArgumentParser(
        description='Process Sonar Project information')
    parser.add_argument('--platform', dest='platform', action='store',
                        nargs='?', default='sonarqube', choices=['sonarqube'])
    parser.add_argument('--project', dest='project', action='store', nargs=1)
    parser.add_argument('--organization', dest='organization',
                        action='store', nargs=1)
    args = parser.parse_args()

    # Start Loggers
    setup_logger()

    with SonarHandler(args) as sonar:
        # Search for project
        if not sonar.autheticated:
            logging.warning('Authentication is not set')
            return

        if not sonar.project:
            logging.warning('The poject has not been set')
            return

        project = sonar.search_project()
        if project:
            logging.info("Project '%s' Already Exists", sonar.project)
            return

        logging.info("Project %s not found, creating", sonar.project)
        sonar_project = sonar.create_project()
        if not sonar_project:
            logging.error("Project not generated")

        logging.info("Project %s has been generated", sonar.project)
        print(sonar_project)


if __name__ == "__main__":
    main()
