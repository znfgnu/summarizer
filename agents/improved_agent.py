import logging

from spade.agent import Agent


class ImprovedAgent(Agent):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("{}:{}".format(self.__class__.__name__, args[0]))
        super().__init__(*args, **kwargs)
        self.logger.info("Hello, world!")
