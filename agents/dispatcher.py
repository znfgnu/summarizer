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
                m = Message(to='chatbot@mokki.org')
                m.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = "pong"
                await self.send(m)

    async def setup(self):
        b = self.RequestBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_CHATBOT_DISPATCHER)
        self.add_behaviour(b, t)
