from system.confidential import TESTING_CREDENTIALS, XMPP_DOMAIN


class CredentialsProvider:
    def __init__(self):
        self.domain = XMPP_DOMAIN
        self.credentials = {
            'testing': iter(TESTING_CREDENTIALS),
        }

    def get_credentials(self, type):
        nickname, password = next(self.credentials[type])
        return "{}@{}".format(nickname, self.domain), password

    def get_testing_credentials(self):
        return self.get_credentials('testing')
