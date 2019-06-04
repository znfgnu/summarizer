# Summarizer

Fetch articles growing in popularity with web-crawling agents and heuristic approach for extractive text summarization.

- Dependencies: [Requirements](requirements.txt)
- Powered by: [PyteaserPython3](https://github.com/alanbuxton/PyTeaserPython3), [News API](https://newsapi.org/), [The New York Times API](https://developer.nytimes.com)

## How to use

### Configuration

######   [New York Times API](https://developer.nytimes.com/get-started) | [News API](https://newsapi.org/) | params: default, filters: article type, sort by newest

1. Provide expected configuration in `config.py` and `stopwords.py.`
2. Prepare API key(s) for News API and/or New York Times API (Article Search). Create `nytimes.api_key` and/or `news.api_key` file(s) and put your credentials inside (plain text).

**Note**:

- **It is possible to operate without any API keys** in test mode (`--test` parameter of script described below).
- News API free plan provides 500 requests per day maximally so for testing purposes, use above parameter.

3. (News API) Check available sources in `news.sources.json`.

**Note**: popular sources: `abc-news, bbc-news, bild, cnn, financial-post, google-news, time, the-new-york-times, the-washington-times`.

### Querying

#### Basic

```bash
python3 main.py -i https://www.nytimes.com/2019/06/01/sports/liverpool-tottenham-champions-league.html
```

Read from web directly, then summarize article.

#### Local merge

```bash
python3 main.py --api local --policy append-by-rank
```

Read from hard-coded input, then summarize and merge summaries of provided articles by ranks of sentences.

#### Test external API

```bash
python3 main.py --api nytimes --test
```

Read hard-coded example API response, then crawl and summarize provided articles by ranks of sentences.

#### External API

```bash
python3 main.py --api nytimes -q "Liverpool Barcelona" --since 20190507 --to 20190507
```

Read from API, then crawl and summarize provided articles by ranks of sentences. Several articles are provided on single page.

#### Full control

```bash
python3 main.py --api news --sources "bbc-news, cnn" -q "Liverpool Barcelona" --since 20190507 --to 20190507 -p 1 -s 4 --policy append-by-rank
```

Read from API, then crawl and summarize provided articles by ranks of sentences. Several articles are provided on single page.

#### Details

Check `python3 main.py -h` to get more help.

- `local` API reads from hard-coded input. `news` is a default API.
- `--policy` - article merge policy (none if not provided).
- `--test` allow you to test without requesting from the API (example responses provided).
- `--ndebug` allows to be more quiet in console.
- `--page`, `--size` allows to specify page number and page size of output from news API.

#### Example

```yaml
python3 main.py --api nytimes -q "Liverpool Barcelona" --since 20190507 --to 20190507
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
