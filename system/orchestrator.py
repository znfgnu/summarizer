import logging
import sys
import time

from system.credentials import CredentialsProvider


class Orchestrator:
    def __init__(self):
        self.credentials = CredentialsProvider()
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        self.logger = logging.getLogger('Orchestrator')
        self.logger.info("Initialized.")

    def start(self):
        self.setup()
        self.run()

    def setup(self):
        self.logger.info("Setting up...")
        # Create all agents
        # - Dispatcher
        # - Judges
        # - Summarizers
        # - Fetchers
        # - Requesters (?)

        self.logger.info("Setup completed.")

    def run(self):
        self.logger.info("Started.")
        while True:
            try:
                time.sleep(3)
                self.logger.info("Still sleeping...")
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt happened.")
                break
        self.logger.info("Goodbye!")
