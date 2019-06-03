from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import pyteaser
from agents.improved_agent import ImprovedAgent
from stopwords import stopwords
from system import global_strings


class Summarizer(ImprovedAgent):
    def __init__(self, config, *args, **kwargs):
        self.configuration = config
        self.summarizer = pyteaser.Summarizer(stopwords, self.configuration)
        super().__init__(*args, **kwargs)

    class SummarizeBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Waiting for requests...")
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.logger.info("Message received with content: {}".format(str(msg)))
                response = self.agent.summarizer.summarize("Test title", msg.body)

                m = Message(to=msg.metadata['to'])
                m.body = '\n'.join(response)
                await self.send(m)

    async def setup(self):
        b = self.SummarizeBehav()
        t = Template()
        t.metadata = {'ontology': global_strings.REQUEST_SUMMARIZE_ONTOLOGY}
        self.add_behaviour(b, t)
