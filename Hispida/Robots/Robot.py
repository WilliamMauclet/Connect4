import logging


class Robot():
    def __init__(self, robotId):
        if robotId is None:
            raise Exception('Please provide an id to the robot.')
        self.robotId = robotId

    def chooseMove(self, grid):
        raise NotImplementedError('Please implement this method in the robot subclass.')

    def log(self, message):
        logging.debug(str(self.__class__.__name__) + self.robotId + ": " + message)

    def get_id_opponent(self):
        if self.robotId == 'X':
            return 'O'
        else:
            'X'
