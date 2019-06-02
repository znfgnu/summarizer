import io

class Article:
    def __init__(self,
                 url,
                 title,
                 content,
                 abstract=None,
                 section=None,
                 subsection=None,
                 pub_date=None):
        self.url = url
        self.title = title
        self.content = content
        self.summary = None
        self.abstract = abstract
        self.section = section
        self.subsection = subsection
        self.pub_date = pub_date

    def set_summary(self, sentences):
        buf = io.StringIO()

        # print(sentences)

        for sentence in sentences:
            print(sentence, file=buf)

        self.summary = buf.getvalue()

        buf.close()


    def __str__(self):
        buf = io.StringIO()

        print('       url: {}'.format(self.url), file=buf)
        if self.section:
            print('   section: {}'.format(self.section), file=buf)
        if self.subsection is not None:
            print('subsection: {}'.format(self.subsection), file=buf)
        if self.pub_date is not None:
            print('  pub date: {}'.format(self.pub_date), file=buf)
        print('     title: {}'.format(self.title), file=buf)
        if self.summary is not None:
            print('   summary:\n{}'.format(self.summary), file=buf)

        str_repr = buf.getvalue()
        buf.close()
        return str_repr
