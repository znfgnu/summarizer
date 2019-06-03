from config import config
from stopwords import stopwords
import argparse
import article
import local
import news
import nytimes
import pyteaser
import utils

debug_more = False


def parse_args(api_call):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--link', type=str,
                        help='Direct link to an article')
    parser.add_argument('-q', type=str,
                        help='Query')
    parser.add_argument('-p', '--page', type=int,
                        help='Number of page')
    parser.add_argument('-s', '--size', type=int,
                        help='(news API) Page size')
    parser.add_argument('--sources', type=str,
                        help='(news API) News sources comma-separated. Popular: '
                        'abc-news, bbc-news, bild, cnn, financial-post, '
                        'google-news, time, the-new-york-times, the-washington-times')
    parser.add_argument('--since', type=str,
                        help='Start date to filter. Example: 20190501')
    parser.add_argument('--to', type=str,
                        help='End date to filter. Example: 20190501')
    parser.add_argument('--api', type=str, choices=api_call.keys(), default='news',
                        help='API Provider (default: news)')
    parser.add_argument('--test', action='store_true',
                        help='Use example response from API (api key not required)')
    parser.add_argument('--ndebug', action='store_true',
                        help='More quiet')
    args = parser.parse_args()

    if args.ndebug is None:
        args.ndebug = False

    global debug_more
    if not args.ndebug:
        debug_more = True

    if args.test:
        return args

    if args.api == 'news':
        # Provide compatible format
        if args.since is not None:
            args.since = '{}-{}-{}'.format(args.since[0:4], args.since[4:6], args.since[6:])
        if args.to is not None:
            args.to = '{}-{}-{}'.format(args.to[0:4], args.to[4:6], args.to[6:])

    if args.api == 'local':
        return args

    if args.size:
        if args.size < 1 or args.size > 100:
            print('Invalid page size! News API supports range: 1-100')
            exit(1)

    if args.link is None and args.q is None:
        print('At least one of pair {link, query} should be provided!')
        exit(1)

    return args


def fetch_directly(link):
    title, content = utils.grab_article(link)
    return [article.Article(link, title, content)]


def fetch_articles(fetcher_response):
    if not fetcher_response:
        return []

    global debug_more
    articles = []
    for r in fetcher_response:
        url = r['url']
        if debug_more:
            print('   Fetching: {}'.format(url))
        title, content = utils.grab_article(url)
        articles.append(article.Article(
            url=url,
            title=title,
            content=content,
            abstract=r['abstract'],
            pub_date=r['pub_date']
        ))
    return articles


def fetch_from_nytimes(args):
    nyTimesApiFetcher = nytimes.ArticleFetcher('nytimes.api_key',
                                               debug=not args.ndebug,
                                               test=args.test)
    response = nyTimesApiFetcher.fetch(query=args.q,
                                       since=args.since,
                                       to=args.to,
                                       page=args.page)
    return fetch_articles(response)


def fetch_from_news(args):
    newsApiFetcher = news.ArticleFetcher(api_key_filename='news.api_key',
                                         sources_filename='news.sources.json',
                                         debug=not args.ndebug,
                                         test=args.test)
    response = newsApiFetcher.fetch(sources=args.sources,
                                    query=args.q,
                                    since=args.since,
                                    to=args.to,
                                    page=args.page,
                                    page_size=args.size)
    return fetch_articles(response)


def print_articles(articles):
    for i in range(len(articles)):
        art = articles[i]
        print('[{}]'.format(i))
        print(art)
        print('   content:')
        print(art.content)


def run_news_api(args):
    # Fetch
    if args.link is not None:
        articles = fetch_directly(args.link)
    else:
        articles = fetch_from_news(args)

    # Summarize
    summarizer = pyteaser.Summarizer(stopwords, config)
    for art in articles:
        sentences = summarizer.summarize(art.title, art.content)
        art.set_summary(sentences)

    # Display
    print_articles(articles)


def run_nytimes_api(args):
    # Fetch
    if args.link is not None:
        articles = fetch_directly(args.link)
    else:
        articles = fetch_from_nytimes(args)

    # Summarize
    summarizer = pyteaser.Summarizer(stopwords, config)
    for art in articles:
        sentences = summarizer.summarize(art.title, art.content)
        art.set_summary(sentences)

    # Display
    print_articles(articles)


def run_local_api(args):
    # Read
    articles = local.articles

    # Summarize
    summarizer = pyteaser.Summarizer(stopwords, config)
    for art in articles:
        sentences = summarizer.summarize(art.title, art.content)
        art.set_summary(sentences)

    # Display
    print_articles(articles)


if __name__ == "__main__":
    api_call = {
        'news': run_news_api,
        'nytimes': run_nytimes_api,
        'local': run_local_api
    }
    try:
        args = parse_args(api_call)
        api_call[args.api](args)
    except KeyboardInterrupt:
        print()
    except IOError:
        print("Please provide valid API key file at first!")
