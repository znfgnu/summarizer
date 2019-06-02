from newsapi import NewsApiClient
import json


class ArticleFetcher:
    LANGUAGE = 'en'  # ar de en es fr he it nl no pt ru se ud zh. Default: all
    SORT_BY = 'relevancy'  # relevancy, popularity, publishedAt. Default: publishedAt
    MAX_SOURCES_NR = 20

    def __init__(self, api_key_filename, sources_filename, debug=False, test=False):
        with open(api_key_filename, 'r') as f:
            api_key = f.readlines()[0].strip()
        with open(sources_filename, 'r') as f:
            sources_json = json.load(f)

        self.debug = debug
        self.client = NewsApiClient(api_key=api_key)
        self.sources = [s['id'] for s in sources_json]
        self.sources_delimited = ''
        self.test = test

        if self.test and self.debug:
            print('   Starting: Test API call (News API)')

    def verify_sources(self, sources):
        if self.debug:
            print('  Verifying: News API sources')
        if sources is None:
            return
        sources = [s.strip() for s in sources.split(',')]
        if len(sources) > 20:
            print('Too many sources! {} is current max'.format(self.MAX_SOURCES_NR))
            exit(1)
        for source in sources:
            self.verify_source(source)

    def verify_source(self, source):
        if source not in self.sources:
            print('Error: source {} not found!'.format(source))
            exit(1)

    def _get_page(self, sources, query, since, to, page, page_size):
        if self.test:
            with open('news.example.json', 'r') as f:
                news_example = json.load(f)
                if self.debug:
                    print('   Fetching: {}'.format(news_example['request']))
                return news_example['response']
        else:
            if self.debug:
                sources_desc = sources if sources else 'all available sources'
                print('   Fetching: {} from {}'.format(query, sources_desc))
            return self.client.get_everything(q=query,
                                              sources=sources,
                                              from_param=since,
                                              to=to,
                                              language=self.LANGUAGE,
                                              sort_by=self.SORT_BY,
                                              page=page,
                                              page_size=page_size)

    def fetch(self,
              sources,
              query,
              since=None,
              to=None,
              page=None,
              page_size=None):
        self.verify_sources(sources)
        res = self._get_page(sources=sources,
                             query=query,
                             since=since,
                             to=to,
                             page=page,
                             page_size=page_size)

        total_res = res['totalResults']
        if total_res == 0:
            return []

        if self.debug:
            print('       Hits: {}'.format(total_res))

        response = []
        for a in res['articles']:
            response.append({
                'url': a['url'],
                'source': a['source'],
                'title': a['title'],
                'abstract': a['description'],
                'pub_date': a['publishedAt']
            })

        return response
