try:
    from system.confidential import TESTING_CREDENTIALS, XMPP_DOMAIN, SUMMARIZER_CREDENTIALS, CHATBOT_CREDENTIALS, \
    DISPATCHER_CREDENTIALS, FETCHER_CREDENTIALS
except ImportError:
    print("Create system/confidential.py based on confidential_template.")


class CredentialsProvider:
    def __init__(self):
        self.domain = XMPP_DOMAIN
        self.credentials = {
            'testing': iter(TESTING_CREDENTIALS),
            'summarizer': iter(SUMMARIZER_CREDENTIALS),
            'chatbot': iter(CHATBOT_CREDENTIALS),
            'dispatcher': iter(DISPATCHER_CREDENTIALS),
            'fetcher': iter(FETCHER_CREDENTIALS),
        }

    def get_credentials(self, type):
        nickname, password = next(self.credentials[type])
        return "{}@{}".format(nickname, self.domain), password

    def get_testing_credentials(self):
        return self.get_credentials('testing')

    def get_summarizer_credentials(self):
        return self.get_credentials('summarizer')

    def get_chatbot_credentials(self):
        return self.get_credentials('chatbot')

    def get_dispatcher_credentials(self):
        return self.get_credentials('dispatcher')

    def get_fetcher_credentials(self):
        return self.get_credentials('fetcher')
