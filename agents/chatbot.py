from spade.behaviour import CyclicBehaviour
from spade.message import Message

from agents.improved_agent import ImprovedAgent
from system import global_strings


class ChatBotAgent(ImprovedAgent):
    class ConversationBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Waiting for message")
            msg = await self.receive(10)
            if msg and msg.body:
                self.agent.logger.info("Query: {}".format(str(msg)))
                m = Message(to=str(msg.sender))
                m.body = "Hello, back!"
                await self.send(m)

                m = Message()
                m.body = msg.body
                m.set_metadata('to', str(msg.sender.bare()))
                m.set_metadata('ontology', global_strings.REQUEST_SUMMARIZE_ONTOLOGY)
                m.to = "summarizer1@mokki.org"
                await self.send(m)
                m.to = "summarizer2@mokki.org"
                await self.send(m)

    def on_subscribe(self, jid):
        self.logger.info("{} asked for subscription.".format(jid))
        self.presence.approve(jid)

    async def setup(self):
        b = self.ConversationBehav()
        self.add_behaviour(b)
        self.presence.on_subscribe = self.on_subscribe
