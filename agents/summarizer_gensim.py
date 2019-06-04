import json

from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from agents.improved_agent import ImprovedAgent
from system import global_strings

from gensim.summarization.summarizer import summarize


class SummarizerGensim(ImprovedAgent):
    class SummarizeBehav(CyclicBehaviour):
        async def run(self):
            self.agent.logger.info("Waiting for requests...")
            msg = await self.receive(timeout=10)
            if msg:
                self.agent.logger.info("Message received with content: {}".format(str(msg)))
                articles = json.loads(msg.body)

                text = '\n'.join([a['content'] for a in articles])

                try:
                    response = summarize(text)
                except:
                    response = ''

                m = Message(to=msg.metadata['judge'])
                m.set_metadata('ontology', global_strings.ONTOLOGY_SUMMARIZER_JUDGE)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = response
                await self.send(m)

    async def setup(self):
        b = self.SummarizeBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_SUMMARIZER)
        self.add_behaviour(b, t)
