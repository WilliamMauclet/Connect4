import os
import sys
import socket

from hispida.grid.Grid import Grid
from hispida.bots.FirstOrderBot import FirstOrderBot as FirstBotClass
from hispida.bots.MinmaxBot import MinmaxBot as SecondBotClass
from threading import Thread


# TODO: testing
bot_ids = ['1', '2']


# TODO: move to test class?
def play_multi():
    thread_first = Thread(target=play, kwargs={'first_not_second': True})
    thread_first.start()
    thread_second = Thread(target=play, kwargs={'first_not_second': False})
    thread_second.start()


def play(first_not_second):
    grid = Grid()
    if first_not_second:
        bot = FirstBotClass(_get_id_from_order(first_not_second))
    else:
        bot = SecondBotClass(_get_id_from_order(first_not_second))
    s = _make_connection(first_not_second)

    if first_not_second:
        bot_move = bot.choose_move(grid)
        grid.add_pawn(bot_move, bot.bot_id)
        s.send(str(bot_move).encode("ascii"))

    try:
        while not grid.game_over():
            opponent_move = int(s.recv(1024).decode("ascii"))  # even 8 (or even 1) should be enough!
            grid.add_pawn(opponent_move, _get_id_opponent(bot.bot_id))

            if grid.game_over():
                break

            bot_move = bot.choose_move(grid)
            grid.add_pawn(bot_move, bot.bot_id)
            s.send(str(bot_move).encode('ascii'))

        print("Winner: " + _get_order_from_id(str(grid.game_over())) + " player: " + str(grid.game_over()))
        print("\nlogs: " + str(grid.logs))
        grid.print_grid()
        s.close()
    except Exception as exc:
        grid.print_grid()
        print("logs: " + str(grid.logs))
        print(exc)


def _get_host_and_port():
    # get local machine name
    host = socket.gethostname()
    port = 9999
    return host, port


def _make_connection(first_not_second):
    if first_not_second:
        return _first_player_connection()
    else:
        return _second_player_connection()


def _first_player_connection():
    # create a socket object
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)

    # bind to the port
    server_socket.bind(_get_host_and_port())
    # queue up to 1 requests
    server_socket.listen(1)

    client_socket = server_socket.accept()[0]

    return client_socket


def _second_player_connection():
    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connection to hostname on the port.
    s.connect(_get_host_and_port())

    return s


def _get_id_opponent(bot_id):
    index = bot_ids.index(bot_id)
    return bot_ids(index + 1 % 2)


def _get_id_from_order(first_not_second):
    index = 0 if first_not_second else 1
    return bot_ids[index]


def _get_order_from_id(bot_id):
    index = bot_ids.index(bot_id)
    if index:
        return 'second'
    else:
        return 'first'


# TODO try-catch in play() to have both bots print their grid so errors can make sense.
play_multi()
