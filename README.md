# Summarizer

Fetch articles growing in popularity with web-crawling agents and heuristic approach for extractive text summarization.

- [Requirements](requirements.txt)

## How to use

### Articles

###### [New York Times API](https://developer.nytimes.com/) | filters: article type, word count between 800 and 5000

1. Prepare API key for New York Times [here](https://developer.nytimes.com/get-started). You need an access to Article Search API.
2. Create `nytimes.api_key` file and put the created key in here.
3. Summarize articles.

```bash
python3 main.py -q <query> [--since <date>] [--to <date>] [-p <pages_limit>]
```

or

```bash
python3 main.py -i <direct_link>
```

### Example

```yaml
python3 main.py -q "Liverpool Barcelona" -p 1 --since 20190507 --to 20190507
    Reading: NYTimes
       Hits: 1
       Docs: 1
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
