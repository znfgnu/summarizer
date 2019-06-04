import logging
import sys
import time

from agents.chatbot import ChatBotAgent
from agents.dispatcher import Dispatcher
from agents.fetchers.nyt_fetcher import NYTFetcherAgent
from agents.summarizer import Summarizer
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
        # - Judges
        # - Summarizers
        # - Fetchers

        jid, passwd = self.credentials.get_summarizer_credentials()
        summarizer1 = Summarizer({
            'ideal_sentences_nr': 5,
            'ideal_sentence_words': 20,
            'num_of_top_keywords': 10,
            'keyword_article_score_multiplier': 1.5,
            'category_weights': {
                'title': 1.5,
                'frequency': 2.0,
                'sentence_length': 1.0,
                'sentence_position': 1.0
            }
        }, jid, passwd)
        # summarizer1.start()

        jid, passwd = self.credentials.get_summarizer_credentials()
        summarizer2 = Summarizer({
            'ideal_sentences_nr': 7,
            'ideal_sentence_words': 15,
            'num_of_top_keywords': 17,
            'keyword_article_score_multiplier': 1.7,
            'category_weights': {
                'title': 1.4,
                'frequency': 1.5,
                'sentence_length': 1.6,
                'sentence_position': 1.8
            }
        }, jid, passwd)
        # summarizer2.start()

        jid, passwd = self.credentials.get_chatbot_credentials()
        chatbot = ChatBotAgent(jid, passwd)
        chatbot.start()

        jid, passwd = self.credentials.get_dispatcher_credentials()
        dispatcher = Dispatcher(jid, passwd)
        dispatcher.start()

        jid, passwd = self.credentials.get_fetcher_credentials()
        nytfetcher = NYTFetcherAgent(jid, passwd)
        nytfetcher.start()

        self.logger.info("Setup completed.")

    def run(self):
        self.logger.info("Started.")
        while True:
            try:
                time.sleep(10)
                self.logger.info("Stayin' alive.")
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt happened.")
                break
        self.logger.info("Goodbye!")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.start()
