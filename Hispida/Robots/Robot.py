import logging


class Robot():
    def __init__(self, robotId):
        self.robotId = robotId

    def chooseMove(self, grid) -> int:
        raise NotImplementedError('Please implement this method in the robot subclass.')

    def log(self, message):
        logging.debug(str(self.__class__.__name__) + self.robotId + ": " + message)

    def get_id_opponent(self) -> str:
        if self.robotId == 'X':
            return 'O'
        else:
            return 'X'

    def get_advanced_description(self):
        return None
