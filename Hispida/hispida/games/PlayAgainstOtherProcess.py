import os
import sys

sys.path.insert(0, os.path.abspath("."))

from Grid import Grid
from hispida.bots.FirstOrderBot import FirstOrderBot as FirstBotClass
from hispida.bots.MinmaxBot import MinmaxBot as SecondBotClass
import socket
from threading import Thread


# TODO: testing

def get_host_and_port():
    # get local machine name
    host = socket.gethostname()
    port = 9999
    return host, port


def make_connection(first_not_second):
    if first_not_second:
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


bot_ids = ['1', '2']


def get_id_opponent(bot_id):
    index = bot_ids.index(bot_id)
    return bot_ids(index + 1 % 2)


def get_id_from_order(first_not_second):
    index = 0 if first_not_second else 1
    return bot_ids[index]


def get_order_from_id(bot_id):
    index = bot_ids.index(bot_id)
    if index:
        return 'second'
    else:
        return 'first'


def play(first_not_second):
    grid = Grid()
    if first_not_second:
        bot = FirstBotClass(get_id_from_order(first_not_second))
    else:
        bot = SecondBotClass(get_id_from_order(first_not_second))
    s = make_connection(first_not_second)

    if first_not_second:
        bot_move = bot.choose_move(grid)
        grid.add_pawn(bot_move, bot.bot_id)
        s.send(str(bot_move).encode("ascii"))

    try:
        while grid.game_over() == -1:
            opponent_move = int(s.recv(1024).decode("ascii"))  # even 8 (or even 1) should be enough!
            grid.add_pawn(opponent_move, get_id_opponent(bot.bot_id))

            if grid.game_over() != -1:
                break

            bot_move = bot.choose_move(grid)
            grid.add_pawn(bot_move, bot.bot_id)
            s.send(str(bot_move).encode('ascii'))

        print("Winner: " + get_order_from_id(str(grid.game_over())) + " player: " + str(grid.game_over()))
        print("logs: " + str(grid.logs))
        grid.print_grid()
        s.close()
    except Exception as exc:
        grid.print_grid()
        print("logs: " + str(grid.logs))
        print(exc)


def play_multi():
    thread_first = Thread(target=play, kwargs={'firstNotSecond': True})
    thread_first.start()
    thread_second = Thread(target=play, kwargs={'firstNotSecond': False})
    thread_second.start()


# TODO try-catch in play() to have both bots print their grid so errors can make sense.

play_multi()
