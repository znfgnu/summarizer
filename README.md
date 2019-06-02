# Summarizer

Fetch articles growing in popularity with web-crawling agents and heuristic approach for extractive text summarization.

- [Requirements](requirements.txt)
- APIs: [News API](https://newsapi.org/), [The New York Times API](https://developer.nytimes.com)

## How to use

### Configuration

###### [PyteaserPython3](https://github.com/alanbuxton/PyTeaserPython3) | params: default

1. ##### Go into `config.py` and `stopwords.py` and provide expected configuration.

***********************

###### [New York Times API](https://developer.nytimes.com/get-started) | [News API](https://newsapi.org/) | filters: article type, sort by newest

2. ##### Prepare API key(s) (depend what you need) for News API and/or New York Times API (you need Article Search API).

**Note**:

- In order to use example API output without providing key, you must provide `--test` parameter.
- News API free plan provides 500 requests per day maximally so for testing purposes, use above parameter.

3. ##### Create `nytimes.api_key` and/or `news.api_key` file(s) and put the created key(s) in here.

4. ##### If you want to use News API, make sure you know the list of available sources in `news.sources.json`.

**Note**: popular sources: `abc-news, bbc-news, bild, cnn, financial-post, google-news, time, the-new-york-times, the-washington-times`.

#### Query

5. ##### Fetch and summarize articles.

```bash
python3 main.py [--api {news,nytimes}] -q <query> [--since <date>] [--to <date>] [--test]
```

**Note**:

- `--test` allow you to test without requesting from the API (example responses provided).
- `news` is a default API.
- `--ndebug` allows to be more quiet in console.
- `--page`, `--size` allows to specify page number and page size of output from news API.

#### Direct link

```bash
python3 main.py -i <direct_link>
```

### Example

```yaml
python3 main.py --api nytimes -q "Liverpool Barcelona"  --since 20190507 --to 20190507
   Fetching: Liverpool Barcelona from the-new-york-times
       Hits: 1
   Fetching: https://www.nytimes.com/2019/05/07/sports/liverpool-barcelona-champions-league.html
[0]
       url: https://www.nytimes.com/2019/05/07/sports/liverpool-barcelona-champions-league.html
  pub date: 2019-05-07T22:46:15+0000
     title: Liverpool Returns to Final, a Shattered Barcelona in Its Wake
   summary:
<summarized content>

   content:
<content>
```
