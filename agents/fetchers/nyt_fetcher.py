import json

from datetime import timedelta, datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

from apis import nytimes
from apis.fetch_articles import fetch_articles
from system import global_strings


class NYTFetcherAgent(Agent):
    class FetchBehav(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(10)

            if msg:
                result = self.agent.article_fetcher.fetch(msg.body, since=datetime.strftime(datetime.now() - timedelta(7), '%Y-%m-%d'))
                articles = fetch_articles(result)

                response = json.dumps([
                    {
                        'title': a.title,
                        'abstract': a.abstract,
                        'content': a.content,
                        'summary': a.summary,
                        'pubdate': a.pub_date,
                    } for a in articles
                ])

                m = Message(to="dispatcher1@mokki.org")
                m.set_metadata('ontology', global_strings.ONTOLOGY_FETCHER_DISPATCHER)
                m.set_metadata('uuid', msg.get_metadata('uuid'))
                m.body = response
                await self.send(m)

    async def setup(self):
        b = self.FetchBehav()
        t = Template()
        t.set_metadata('ontology', global_strings.ONTOLOGY_DISPATCHER_FETCHER)
        self.add_behaviour(b, t)

    def __init__(self, *args, **kwargs):
        self.article_fetcher = nytimes.ArticleFetcher()
        super().__init__(*args, **kwargs)
