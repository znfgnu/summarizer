from PyTeaserPython3 import pyteaser
from gensim.summarization.summarizer import summarize

urls = []
urls.append('http://www.espnfc.com/english-premier-league/23/blog/post/3862792/champions-league-europa-league-success-for-arsenal-chelsea-and-spurs-shows-power-of-london-effect')
# urls.append('https://rare-technologies.com/text-summarization-in-python-extractive-vs-abstractive-techniques-revisited/')

results_pyteaser = {}
results_gensim = {}


def grab_link(inurl):
    from goose import Goose
    try:
        article = Goose().extract(url=inurl)
        return article
    except ValueError:
        print('Goose failed to extract article from url')
        return None
    return None


def print_result(sentences, array=False):
    if sentences is None:
        return
    if not array:
        print(sentences)
        return
    for sentence in sentences:
        print(sentence)


def summarize_pyteaser(url):
    return pyteaser.SummarizeUrl(url)


def summarize_gensim(url):
    return summarize(article.cleaned_text)


if __name__ == "__main__":
    for url in urls:
        try:
            article = grab_link(url)
        except IOError:
            print('IOError')
            exit(1)

        results_pyteaser[url] = summarize_pyteaser(url)
        results_gensim[url] = summarize_gensim(url)

    for res in results_pyteaser:
            print('----- PYTEASER ------')
            print_result(results_pyteaser[res], array=True)
            print()

    for res in results_gensim:
            print('----- GENSIM ------')
            print_result(results_gensim[res])
            print()
