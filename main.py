from PyTeaserPython3 import pyteaser

urls = []
urls.append('http://www.espnfc.com/english-premier-league/23/blog/post/3862792/champions-league-europa-league-success-for-arsenal-chelsea-and-spurs-shows-power-of-london-effect')
urls.append('https://rare-technologies.com/text-summarization-in-python-extractive-vs-abstractive-techniques-revisited/')

results_pyteaser = {}


def print_result(sentences):
    if sentences is None:
        return
    for sentence in sentences:
        print(sentence)


def summarize_pyteaser(url):
    return pyteaser.SummarizeUrl(url)


if __name__ == "__main__":
    for url in urls:
        results_pyteaser[url] = summarize_pyteaser(url)

    for res in results_pyteaser:
            print_result(results_pyteaser[res])
            print()
