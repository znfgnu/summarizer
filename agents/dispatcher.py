from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from agents.improved_agent import ImprovedAgent
from system import global_strings


class Dispatcher(ImprovedAgent):
    class RequestBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Dispatcher waiting for requests...")
            msg = await self.receive(10)

            if msg:
                m = Message(to='fetcher1@mokki.org')
                m.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_FETCHER)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = "FC Barcelona"
                await self.send(m)

    class ArticlesBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(10)

            if msg:
                # mock ; return to chatbot
                m = Message(to="chatbot@mokki.org")
                m.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = msg.body
                await self.send(m)

    async def setup(self):
        b = self.RequestBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_CHATBOT_DISPATCHER)
        self.add_behaviour(b, t)

        b = self.ArticlesBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_FETCHER_DISPATCHER)
        self.add_behaviour(b, t)
