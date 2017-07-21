import logging

from gi.overrides import deprecated


class Bot:
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def choose_move(self, grid) -> int:
        raise NotImplementedError('Please implement this method in subclass.')

    def log(self, message) -> None:
        logging.debug(str(self.__class__.__name__) + self.bot_id + ": " + message)

    # TODO replace with is_id_opponent?
    @deprecated
    def get_id_opponent(self) -> str:
        """
        TODO: replace with is_id_opponent'
        """
        if self.bot_id == 'X':
            return 'O'
        else:
            return 'X'

    def is_id_opponent(self, bot_id: str) -> bool:
        return bot_id != '_' and bot_id != self.bot_id

    def get_configuration(self) -> dict:
        return {}
