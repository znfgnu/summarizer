import json
import requests


class ArticleFetcher:
    SOURCE = 'the-new-york-times'
    BASE = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    FILTER_QUERY = 'document_type:("article")'
    SORT = 'newest'

    def __init__(self, api_key_filename, debug=False, test=False):
        with open(api_key_filename, 'r') as f:
            api_key = f.readlines()[0].strip()
        self.api_key = api_key
        self.debug = debug
        self.test = test

        if self.test and self.debug:
            print('   Starting: Test API call (NYTimes)')

    def _get_page(self, query, since, to, page):
        if self.test:
            with open('nytimes.example.json', 'r') as f:
                nytimes_example = json.load(f)
                if self.debug:
                    print('   Fetching: {}'.format(nytimes_example['request']))
                return nytimes_example['response']['response']
        else:
            if self.debug:
                print('   Fetching: {} from {}'.format(query, self.SOURCE))

            request_content = '{}?q={}&fq={}&sort={}'.format(
                    self.BASE,
                    query,
                    self.FILTER_QUERY,
                    self.SORT)

            if since is not None:
                request_content += '&begin_date={}'.format(since)
            if to is not None:
                request_content += '&end_date={}'.format(to)
            if page is not None:
                request_content += '&page={}'.format(page)

            request_content += '&api-key={}'.format(self.api_key)

            res = requests.get(request_content)

            if res.status_code != 200:
                res.raise_for_status()

            return res.json()['response']

    def fetch(self,
              query,
              since=None,
              to=None,
              page=None):
        res = self._get_page(query,
                             since=since,
                             to=to,
                             page=page)

        total_res = res['meta']['hits']
        if total_res == 0:
            return []

        docs = res['docs']
        response = []
        for doc in docs:
            response.append({
                'url': doc['web_url'],
                'source': self.SOURCE,
                'title': doc['lead_paragraph'],
                'abstract': doc['abstract'],
                'pub_date': doc['pub_date']
            })

        return response
