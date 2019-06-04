from apis import utils, article


def fetch_articles(fetcher_response):
    if not fetcher_response:
        return []

    articles = []
    for r in fetcher_response:
        url = r['url']
        title, content = utils.grab_article(url)
        articles.append(article.Article(
            url=url,
            title=title,
            content=content,
            abstract=r['abstract'],
            pub_date=r['pub_date']
        ))
    return articles
