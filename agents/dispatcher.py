import datetime
import json

import dateparser
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from agents.improved_agent import ImprovedAgent
from system import global_strings


class DispatcherState:
    def __init__(self, responses_needed, timeout):
        self.responses_needed = responses_needed
        self.responses_received = 0
        self.articles = []
        self.endtime = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    def is_ready_to_go(self):
        return self.responses_needed == self.responses_received

    def is_timed_out(self):
        return datetime.datetime.now() > self.endtime

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
                self.agent.sessions[request_uuid] = DispatcherState(2, 30)

                m = Message()
                m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_FETCHER)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = msg.body
                m.to = 'fetcher1@mokki.org'
                await self.send(m)
                m.to = 'fetcher2@mokki.org'
                await self.send(m)

    class ArticlesBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(1)

            if msg:
                request_uuid = msg.get_metadata('uuid')
                if request_uuid in self.agent.sessions:
                    articles = json.loads(msg.body)
                    self.agent.sessions[request_uuid].add_response(articles)
                    self.agent.logger.info("Dispatcher received articles {}/{}".format(self.agent.sessions[request_uuid].responses_received, self.agent.sessions[request_uuid].responses_needed))
                else:
                    self.agent.logger.warn("woot woot {}".format(str(msg)))

            to_remove = []
            for uuid, ds in self.agent.sessions.items():
                if ds.is_ready_to_go() or ds.is_timed_out():
                    articles_list = ds.get_sorted_articles()
                    response = json.dumps(articles_list)

                    # For now the same response goes to both: judges and summarizers:

                    # 1. Judge
                    m = Message()
                    m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_JUDGE)
                    m.set_metadata('uuid', uuid)
                    m.set_metadata('timeout', '10')
                    m.set_metadata('summarizers', '5')
                    m.body = response

                    m.to = 'judge1@mokki.org'
                    await self.send(m)

                    # 2. summarizers
                    m = Message()
                    m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_SUMMARIZER)
                    m.set_metadata('uuid', uuid)
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

                    # mock ; return to chatbot
                    # m.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
                    # m.to = 'chatbot@mokki.org'
                    # await self.send(m)

                    # remove session - not needed anymore
                    to_remove.append(uuid)

            for uuid in to_remove:
                del self.agent.sessions[uuid]

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