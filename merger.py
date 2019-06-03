class Merger:
    POLICIES = {
        'append': None,
        'append-by-rank': None
    }

    def __init__(self, policy, max_articles_in_single_summary=5):
        self.POLICIES['append'] = self._append
        self.POLICIES['append-by-rank'] = self._append_by_rank

        if policy not in self.POLICIES:
            print('Error: invalid article merge policy. Available ones: {}'.format(
                    str(self.POLICIES.keys())[1:-1]))
            exit(1)

        self.policy = policy
        self.max_articles_summary_size = max_articles_in_single_summary

    def _append(self, sentences_list):
        final_summary = ''

        for sentences in sentences_list:
            for sentence in sentences:
                final_summary += sentence + '\n'

        return final_summary

    def _append_by_rank(self, sentences_list):
        final_summary = ''

        for j in range(self.max_articles_summary_size):
            for i in range(len(sentences_list)):
                if j < len(sentences_list[i]):
                    final_summary += sentences_list[i][j] + '\n'

        return final_summary

    def merge(self, articles):
        sentences_list = []

        for art in articles:
            sentences_list.append(art.summary.split('\n'))

        return self.POLICIES[self.policy](sentences_list)
