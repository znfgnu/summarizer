import requests
from article import Article
from goose import Goose


class ArticleFetcher:
    BASE = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    FILTER_QUERY = 'document_type:("article") AND word_count:[800 TO 5000]'
    HITS_ON_PAGE = 10

    def __init__(self, api_key_filename, debug=False):
        with open(api_key_filename, 'r') as f:
            api_key = f.readlines()[0].strip()

        self.api_key = api_key
        self.debug = debug

    def _grab_article(self, url):
        try:
            extraction = Goose().extract(url=url)

            if not (extraction and extraction.cleaned_text and extraction.title):
                return None, None

            return extraction.title, extraction.cleaned_text
        except ValueError:
            pass
        return None, None

    def _get_first_page(self, query, since=None, to=None):
        if self.debug:
            print('    Reading: NYTimes')

        request_content = '{}?q={}&fq={}&api-key={}'.format(
                self.BASE,
                query,
                self.FILTER_QUERY,
                self.api_key)

        if since is not None:
            request_content += '&begin_date={}'.format(since)
        if to is not None:
            request_content += '&end_date={}'.format(to)

        res = requests.get(request_content)

        if res.status_code != 200:
            res.raise_for_status()

        self.response = res.json()['response']
        self.docs = self.response['docs']
        self.meta = self.response['meta']
        self.hits = self.meta['hits']
        self.pages = int(self.hits / self.HITS_ON_PAGE) + 1

    def _get_page(self, query, nr, since=None, to=None):
        request_content = '{}?q={}&fq={}&api-key={}'.format(
                self.BASE,
                query,
                self.FILTER_QUERY,
                self.api_key)

        request_content += '&page={}'.format(nr)
        if since is not None:
            request_content += '&begin_date={}'.format(since)
        if to is not None:
            request_content += '&end_date={}'.format(to)

        res = requests.get(request_content)

        if res.status_code != 200:
            res.raise_for_status()

        self.response = res.json()['response']
        return self.response['docs']

    def _fetch_articles(self):
        articles = []

        for doc in self.docs:
            url = doc['web_url']

            if self.debug:
                print('   Fetching: {}'.format(url))

            title, content = self._grab_article(url)
            articles.append(Article(
                url=url,
                title=title,
                content=content,
                abstract=doc['abstract'] if 'abstract' in doc else None,
                section=doc['section'] if 'section' in doc else None,
                subsection=doc['subsection'] if 'subsection' in doc else None,
                pub_date=doc['pub_date'] if 'pub_date' in doc else None
            ))

        if self.debug:
            print()

        return articles

    def fetch(self, query, pages_limit=None, since=None, to=None):
        self._get_first_page(query, since, to)

        if pages_limit > self.pages:
            pages_limit = self.pages

        if self.debug:
            print('       Hits: {}'.format(self.hits))

        if len(self.docs) == 0:
            return []

        if self.debug:
            docs_nr = pages_limit * self.HITS_ON_PAGE
            if docs_nr > self.hits:
                docs_nr = self.hits
            print('       Docs: {}'.format(docs_nr))

        for i in range(2, pages_limit + 1):
            self.docs.extend(self._get_page(query, i, since, to))

        return self._fetch_articles()
