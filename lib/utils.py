import os


def get_token():
    """ Retrives the SONAR_TOKEN value """
    return os.getenv('SONAR_TOKEN')