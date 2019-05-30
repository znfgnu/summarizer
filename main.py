from nytimes import ArticleFetcher
from pyteaser import Summarizer
from config import config
from stopwords import stopwords
import argparse
import article
import utils


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--link', type=str,
                        help='Direct link to an article')
    parser.add_argument('-q', '--query', type=str,
                        help='Query')
    parser.add_argument('-p', '--pages_limit', type=int, default=1,
                        help='Maximal number of pages')
    parser.add_argument('--since', type=str,
                        help='Start date to filter. Example: 20190501')
    parser.add_argument('--to', type=str,
                        help='End date to filter. Example: 20190501')
    args = parser.parse_args()

    if args.link is None and args.query is None:
        print('At least one of pair {link, query} should be provided!')
        exit(1)

    return args


if __name__ == "__main__":
    args = parse_args()
    try:
        fetcher = ArticleFetcher('nytimes.api_key', debug=True)
        summarizer = Summarizer(stopwords, config)

        if args.link is not None:
            title, content = utils.grab_article(args.link)
            articles = [article.Article(args.link, title, content)]
        else:
            articles = fetcher.fetch(query=args.query,
                                     pages_limit=args.pages_limit,
                                     since=args.since,
                                     to=args.to)
        summaries = {}

        for i in range(len(articles)):
            article = articles[i]
            sentences = summarizer.summarize(article.title, article.content)
            article.set_summary(sentences)

            print('[{}]'.format(i))
            print(article)
            print('   content:')
            print(article.content)
    except IOError:
        print("Please provide NYTimes API key in 'nytimes.api_key' file!")
        print('You need an access to Article Search API.')
        print('https://developer.nytimes.com/apis')
    except KeyboardInterrupt:
        print()
