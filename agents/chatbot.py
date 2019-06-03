import uuid

from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from agents.improved_agent import ImprovedAgent
from system import global_strings


class ChatBotAgent(ImprovedAgent):
    class ConversationBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Waiting for message")
            msg = await self.receive(10)
            # No metadata means request from user
            if msg and msg.body and not msg.metadata:
                self.agent.logger.info("Query: {}".format(str(msg)))
                m = Message(to=str(msg.sender))
                m.body = "Hello, back! We're preparing summary for the topic you chose!"
                await self.send(m)

                request_uuid = uuid.uuid4()
                self.agent.sessions[str(request_uuid)] = str(msg.sender)

                m = Message()
                m.body = msg.body
                m.set_metadata('uuid', str(request_uuid))
                m.set_metadata('ontology', global_strings.ONTOLOGY_CHATBOT_DISPATCHER)
                m.to = "dispatcher1@mokki.org"
                await self.send(m)

    class ResponseBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Waiting for judgement...")
            msg = await self.receive(10)

            if msg:
                self.agent.logger.info("Judgement: {}".format(str(msg)))
                request_uuid = msg.get_metadata('uuid')
                user = self.agent.sessions[request_uuid]

                m = Message(to=user)
                # only forwarding, can be formatted TODO
                m.body = msg.body
                await self.send(m)

                del self.agent.sessions[request_uuid]

    def on_subscribe(self, jid):
        self.logger.info("{} asked for subscription.".format(jid))
        self.presence.approve(jid)

    async def setup(self):
        b = self.ConversationBehav()
        self.add_behaviour(b)

        b = self.ResponseBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_JUDGE_CHATBOT)
        self.add_behaviour(b, t)

        self.presence.on_subscribe = self.on_subscribe

    def __init__(self, *args, **kwargs):
        self.sessions = {}
        super().__init__(*args, **kwargs)
