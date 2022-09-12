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
    logger.addHandler(RotatingFileHandler('master.log', maxBytes=2000000, backupCount=10))

    # Add stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

def validate(args):
    """ Validate Inputs """
    if not getattr(args, 'project'):
        raise argparse.ArgumentError(None, 'Project is mandatory')


def main():
    """ Entry Point """
    parser = argparse.ArgumentParser(description='Process Sonar Project information')
    parser.add_argument('--project', dest='project', action='store', nargs=1)
    args = parser.parse_args()

    # Validate Inputs
    validate(args)

    # Start Loggers
    setup_logger()

    project = args.project[-1]
    with SonarHandler(project) as sonar:

        # Search for project
        if sonar.autheticated:
            projects = sonar.search_project(project)

            # Filter for exact match
            match = list(filter(lambda p: p.key == project, projects))
            if not match:
                logging.info(f'Project {project} not found, creating')
                sonar_project = sonar.create_project(project)
                print(sonar_project)


if __name__ == "__main__":
    main()
