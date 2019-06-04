import asyncio
import json

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
            # self.agent.logger.info("Waiting for requests...")
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.logger.info("Message received")
                articles = json.loads(msg.body)

                text = '\n'.join([a['content'] for a in articles])

                response = self.agent.summarizer.summarize("Test title", text)

                m = Message(to=msg.metadata['judge'])
                m.set_metadata('ontology', global_strings.ONTOLOGY_SUMMARIZER_JUDGE)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = '\n'.join(response)
                await self.send(m)
                self.agent.logger.info("Response sent!")

    async def setup(self):
        b = self.SummarizeBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_SUMMARIZER)
        self.add_behaviour(b, t)
