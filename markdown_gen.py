class MarkdownGenerator:
    def generate(self, f, args, articles, final_summary):
        print('# Summarizer', file=f)
        print(file=f)

        if final_summary:
            print('## Merged summary', file=f)
            print(file=f)
            print(final_summary, file=f)
            print(file=f)

        print('## Articles', file=f)
        print(file=f)
        for article in articles:
            print(article.markdown(), file=f)
