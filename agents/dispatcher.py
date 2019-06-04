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
            msg = await self.receive(10)

            if msg:
                self.agent.logger.info("Dispatcher got request!")
                request_uuid = msg.get_metadata('uuid')
                self.agent.sessions[request_uuid] = DispatcherState(1)

                m = Message()
                m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_FETCHER)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = msg.body
                m.to = 'fetcher1@mokki.org'
                await self.send(m)
                # m.to = 'fetcher2@mokki.org'
                # await self.send(m)

    class ArticlesBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(10)

            if msg:
                request_uuid = msg.get_metadata('uuid')
                articles = json.loads(msg.body)
                self.agent.sessions[request_uuid].add_response(articles)
                self.agent.logger.info("Dispatcher received articles {}/{}".format(self.agent.sessions[request_uuid].responses_received, self.agent.sessions[request_uuid].responses_needed))

                if self.agent.sessions[request_uuid].is_ready_to_go():
                    articles_list = self.agent.sessions[request_uuid].get_sorted_articles()
                    response = json.dumps(articles_list)

                    # For now the same response goes to both: judges and summarizers:
                    # 1. summarizers
                    m = Message()
                    m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_SUMMARIZER)
                    m.set_metadata('uuid', request_uuid)
                    m.set_metadata('judge', 'judge1@mokki.org')
                    m.body = response

                    m.to = 'summarizer1@mokki.org'
                    await self.send(m)
                    m.to = 'summarizer2@mokki.org'
                    await self.send(m)
                    m.to = 'summarizer3@mokki.org'
                    await self.send(m)
                    m.to = 'summarizer4@mokki.org'
                    await self.send(m)
                    m.to = 'summarizer5@mokki.org'
                    await self.send(m)

                    # 2. Judge
                    m = Message()
                    m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_JUDGE)
                    m.set_metadata('uuid', request_uuid)
                    # m.set_metadata('timeout', '20')
                    m.set_metadata('summarizers', '5')
                    m.body = response

                    m.to = 'judge1@mokki.org'
                    await self.send(m)

                    # mock ; return to chatbot
                    # m.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
                    # m.to = 'chatbot@mokki.org'
                    # await self.send(m)

                    # remove session - not needed anymore
                    del self.agent.sessions[request_uuid]

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