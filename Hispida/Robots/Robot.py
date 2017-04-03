import logging


class Robot():
    def __init__(self, robot_id):
        self.robot_id = robot_id

    def chooseMove(self, grid) -> int:
        raise NotImplementedError('Please implement this method in the robot subclass.')

    def log(self, message) -> None:
        logging.debug(str(self.__class__.__name__) + self.robot_id + ": " + message)

    def get_id_opponent(self) -> str:
        if self.robot_id == 'X':
            return 'O'
        else:
            return 'X'

    def get_configuration(self) -> dict:
        return {}
