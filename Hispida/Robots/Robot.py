class Robot():

    def __init__(self, robotId):
        if robotId is None:
            raise Exception('Please provide an id to the robot.')
        self.robotId = robotId

    def chooseMove(self, grid):
        raise NotImplementedError('Please implement this method in the robot subclass.')

    def get_id_opponent(self):
        if self.robotId == 'X':
            return 'O'
        else:
            'X'