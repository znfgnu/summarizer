import json

import dateparser
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from agents.improved_agent import ImprovedAgent
from system import global_strings


class DispatcherState:
    def __init__(self, responses_needed):
        self.responses_needed = responses_needed
        self.responses_received = 0
        self.articles = []

    def is_ready_to_go(self):
        return self.responses_needed == self.responses_received

    def add_response(self, response):
        self.articles += response
        self.responses_received += 1

    def get_sorted_articles(self):
        return list(sorted(self.articles, key=lambda a: dateparser.parse(a['pubdate'])))


class Dispatcher(ImprovedAgent):
    class RequestBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Dispatcher waiting for requests...")
            msg = await self.receive(10)

            if msg:
                request_uuid = msg.get_metadata('uuid')
                self.agent.sessions[request_uuid] = DispatcherState(2)

                m = Message()
                m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_FETCHER)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = "FC Barcelona"
                m.to = 'fetcher1@mokki.org'
                await self.send(m)
                m.to = 'fetcher2@mokki.org'
                await self.send(m)

    class ArticlesBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(10)

            if msg:
                request_uuid = msg.get_metadata('uuid')
                articles = json.loads(msg.body)
                self.agent.sessions[request_uuid].add_response(articles)

                if self.agent.sessions[request_uuid].is_ready_to_go():
                    articles_list = self.agent.sessions[request_uuid].get_sorted_articles()
                    response = json.dumps(articles_list)
                    # For now the same response goes to both: judges and summarizers
                    # ...soon

                    # mock ; return to chatbot
                    m = Message(to="chatbot@mokki.org")
                    m.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
                    m.set_metadata('uuid', request_uuid)
                    m.body = str(response)
                    await self.send(m)

                    # 1. summarizers
                    # 2. judge
                    # remove session - not needed anymore

    async def setup(self):
        b = self.RequestBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_CHATBOT_DISPATCHER)
        self.add_behaviour(b, t)

        b = self.ArticlesBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_FETCHER_DISPATCHER)
        self.add_behaviour(b, t)

    def __init__(self, *args, **kwargs):
        self.sessions = {}
        super().__init__(*args, **kwargs)