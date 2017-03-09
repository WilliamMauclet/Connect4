import sys,os
sys.path.insert(0, os.path.abspath("."))

from Grid.Grid import ColumnGrid
from Robots.FirstOrderRobot import FirstOrderRobot
import socket

# TODO both first and second player must connect and listen!
# TODO is socket bi-directional? YES
# 1) P1 starts and listens
# 2) P2 starts and makes connection
#

def make_connection(firstNotSecond):
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # get local machine name
    host = socket.gethostname()
    if firstNotSecond:
        port = 9998
        # bind to the port
        s.bind((host, port))
        # queue up to 5 requests
        s.listen(1)
        s = s.accept()

        # TODO
        s.send(str.encode("CHOSEN FIRST MOVE"))
    else:
        port = 9999
        s.connect((host, port))
    return s

def first_player_make_connection():
    # create a socket object
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    port = 9999

    # bind to the port
    serversocket.bind((host, port))

    # queue up to 1 requests
    serversocket.listen(1)

def play(firstNotSecond):
    grid = ColumnGrid()
    robot = FirstOrderRobot('X')


    s = make_connection(firstNotSecond)

    while not grid.game_over():

        opponent_move = int(s.recv(1024)) # even 8 (or even 1) should be enough!

        grid.add_pawn(opponent_move, 'O')

        if grid.game_over():
            break

        robot_move = str(robot.choose_move(grid))
        s.send(robot_move.encode('ascii'))
        break

    s.close()





play(True)