from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from agents.improved_agent import ImprovedAgent
from system import global_strings


class SenderAgent(ImprovedAgent):
    class SendBehav(PeriodicBehaviour):
        async def run(self):
            m = Message(to="summarizer1@mokki.org")
            m.set_metadata('ontology', global_strings.REQUEST_SUMMARIZE_ONTOLOGY)
            m.body = "Hello, there!"
            await self.send(m)
            self.agent.logger.info("Sent.")

    async def setup(self):
        b = self.SendBehav(period=5)
        self.add_behaviour(b)
