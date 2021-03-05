import time

from app.models import Session


class SessionManager:
    __instance = None
    session = None
    isBeingUsed = False

    @staticmethod
    def yield_session():
        if SessionManager.__instance is not None:
            SessionManager.__instance.isBeingUsed = False

    @staticmethod
    def get_session():
        """ Static access method. """
        if SessionManager.__instance is None:
            SessionManager()
        while SessionManager.__instance.isBeingUsed:
            time.sleep(5)
        SessionManager.__instance.isBeingUsed = True
        return SessionManager.__instance.session

    def __init__(self):
        """ Virtually private constructor. """
        if SessionManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SessionManager.__instance = self
            SessionManager.__instance.session = Session()
            SessionManager.__instance.isBeingUsed = False

    def __del__(self):
        SessionManager.__instance.session.close()
