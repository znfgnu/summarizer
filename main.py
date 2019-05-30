from PyTeaserPython3 import pyteaser
from nytimes import ArticleFetcher
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type=str, required=True,
                        help='Query')
    parser.add_argument('-p', '--pages_limit', type=int, default=1,
                        help='Maximal number of pages')
    parser.add_argument('--since', type=str,
                        help='Start date to filter. Example: 20190501')
    parser.add_argument('--to', type=str,
                        help='End date to filter. Example: 20190501')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        fetcher = ArticleFetcher('nytimes.api_key', debug=True)
        articles = fetcher.fetch(query=args.query,
                                 pages_limit=args.pages_limit,
                                 since=args.since,
                                 to=args.to)
        summaries = {}

        for i in range(len(articles)):
            article = articles[i]
            sentences = pyteaser.Summarize(article.title, article.content)

            summary = ''
            for sentence in sentences:
                summary += '{} '.format(sentence)

            article.set_summary(summary)

            print('[{}]'.format(i))
            print(article)
            print('   content:')
            print(article.content)
            print()
    except IOError:
        print("Please provide NYTimes API key in 'nytimes.api_key' file!")
        print('You need an access to Article Search API.')
        print('https://developer.nytimes.com/apis')
    except KeyboardInterrupt:
        print()
