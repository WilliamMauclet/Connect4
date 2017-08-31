import logging


class Bot:
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def choose_move(self, grid) -> int:
        raise NotImplementedError('Please implement this method in subclass.')

    def get_configuration(self) -> dict:
        return {}

    def get_descriptor(self) -> str:
        return self.__class__.__name__

    def _is_id_opponent(self, bot_id: str) -> bool:
        return bot_id != '_' and bot_id != self.bot_id

    def _log(self, message) -> None:
        logging.debug(str(self.__class__.__name__) + self.bot_id + ": " + message)
