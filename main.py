import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys

from lib.handler import SonarHandler


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Add log file
    logger.addHandler(RotatingFileHandler('master.log', maxBytes=2000000, backupCount=10))

    # Add stdout
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def main():
    """ Entry Point """
    parser = argparse.ArgumentParser(description='Process Sonar Project information')
    parser.add_argument('--project', dest='project', action='store', nargs=1)
    args = parser.parse_args()

    # Validate Inputs
    project = args.project

    # Start Loggers
    setup_logger()

    with SonarHandler(project) as sonar:
        sonar

if __name__ == "__main__":
    main()