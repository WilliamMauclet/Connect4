import sys, os

sys.path.insert(0, os.path.abspath("."))

from Grid.Grid import ColumnGrid
from Robots.FirstOrderRobot import FirstOrderRobot
import socket
from threading import Thread


def get_host_and_port():
    # get local machine name
    host = socket.gethostname()
    port = 9999
    return (host, port)


def make_connection(firstNotSecond):
    if firstNotSecond:
        return first_player_connection()
    else:
        return second_player_connection()


def first_player_connection():
    # create a socket object
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # bind to the port
    server_socket.bind(get_host_and_port())
    # queue up to 1 requests
    server_socket.listen(1)

    client_socket = server_socket.accept()[0]

    return client_socket


def second_player_connection():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to hostname on the port.
    s.connect(get_host_and_port())

    return s


def get_id_from_order(firstNotSecond):
    if firstNotSecond:
        return 'X'
    else:
        return 'O'


def get_order_from_id(id):
    if id == 'X':
        return 'first'
    else:
        return 'second'


def play(firstNotSecond):
    grid = ColumnGrid()
    robot = FirstOrderRobot(get_id_from_order(firstNotSecond))

    s = make_connection(firstNotSecond)

    if firstNotSecond:
        robot_move = str(robot.choose_move(grid))
        s.send(robot_move.encode("ascii"))

    while grid.game_over() == -1:
        opponent_move = int(s.recv(1024).decode("ascii"))  # even 8 (or even 1) should be enough!
        grid.add_pawn(opponent_move, robot.get_id_opponent())

        if grid.game_over() != -1:
            break

        robot_move = robot.choose_move(grid)
        grid.add_pawn(robot_move, robot.robotId)
        s.send(str(robot_move).encode('ascii'))

    print("Winner: " + get_order_from_id(str(grid.game_over())) + " player: " + str(grid.game_over()))
    print(grid.print_grid())
    s.close()


def play_multi():
    thread_first = Thread(target=play, kwargs={'firstNotSecond': True})
    thread_first.start()
    thread_second = Thread(target=play, kwargs={'firstNotSecond': False})
    thread_second.start()


play_multi()
