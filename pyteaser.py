from collections import Counter
from math import fabs
import utils


class Summarizer:
    '''
    Remastered pyteaser module originally made by alanbuxton.
    '''
    def __init__(self, stopwords, config):
        self.stopwords = stopwords
        self.ideal_sentences_nr = config['ideal_sentences_nr']
        self.ideal_sentence_words = config['ideal_sentence_words']
        self.num_top = config['num_of_top_keywords']
        self.keyword_article_score_multiplier = config['keyword_article_score_multiplier']
        self.weight_title = config['category_weights']['title']
        self.weight_frequency = config['category_weights']['frequency']
        self.weight_sentence_length = config['category_weights']['sentence_length']
        self.weight_sentence_position = config['category_weights']['sentence_position']

    def _keywords(self, text):
        """get the top keywords and their frequency scores
        ignores blacklisted words in stopwords,
        counts the number of occurrences of each word
        """
        text = utils.split_words(text)
        words_before_blacklist_removal = len(text)
        freq = Counter(x for x in text if x not in self.stopwords)
        minSize = min(self.num_top, len(freq))

        # recreate a dict
        keywords = {x: y for x, y in freq.most_common(minSize)}

        for k in keywords:
            articleScore = keywords[k] * 1.0 / words_before_blacklist_removal
            keywords[k] = articleScore * self.keyword_article_score_multiplier + 1

        return keywords

    def _length_score(self, sentence):
        return 1 - fabs(self.ideal_sentence_words - len(sentence)) / self.ideal_sentence_words

    def _title_score(self, title, sentence):
        title = [x for x in title if x not in self.stopwords]
        count = 0.0
        for word in sentence:
            if (word not in self.stopwords and word in title):
                count += 1.0

        if len(title) == 0:
            return 0.0

        return count/len(title)

    def _sentence_position(self, i, size):
        """different sentence positions indicate different
        probability of being an important sentence"""

        normalized = i*1.0 / size
        if 0 < normalized <= 0.1:
            return 0.17
        elif 0.1 < normalized <= 0.2:
            return 0.23
        elif 0.2 < normalized <= 0.3:
            return 0.14
        elif 0.3 < normalized <= 0.4:
            return 0.08
        elif 0.4 < normalized <= 0.5:
            return 0.05
        elif 0.5 < normalized <= 0.6:
            return 0.04
        elif 0.6 < normalized <= 0.7:
            return 0.06
        elif 0.7 < normalized <= 0.8:
            return 0.04
        elif 0.8 < normalized <= 0.9:
            return 0.04
        elif 0.9 < normalized <= 1.0:
            return 0.15
        else:
            return 0

    def _sbs(self, words, keywords):
        score = 0.0
        if len(words) == 0:
            return 0
        for word in words:
            if word in keywords:
                score += keywords[word]
        return (1.0 / fabs(len(words)) * score) / self.num_top

    def _dbs(self, words, keywords):
        if (len(words) == 0):
            return 0

        summ = 0
        first = []
        second = []

        for i, word in enumerate(words):
            if word in keywords:
                score = keywords[word]
                if first == []:
                    first = [i, score]
                else:
                    second = first
                    first = [i, score]
                    dif = first[0] - second[0]
                    summ += (first[1]*second[1]) / (dif ** 2)

        # number of intersections
        k = len(set(keywords.keys()).intersection(set(words))) + 1
        return (1/(k*(k+1.0))*summ)

    def _score(self, sentences, titleWords, keywords):
        # score sentences based on different features

        senSize = len(sentences)
        ranks = Counter()
        for i, s in enumerate(sentences):
            sentence = utils.split_words(s)
            titleFeature = self._title_score(titleWords, sentence)
            sentenceLength = self._length_score(sentence)
            sentencePosition = self._sentence_position(i+1, senSize)
            sbsFeature = self._sbs(sentence, keywords)
            dbsFeature = self._dbs(sentence, keywords)
            frequency = (sbsFeature + dbsFeature) / 2.0 * self.num_top

            # weighted average of scores from four categories
            totalScore = (titleFeature * self.weight_title + frequency * self.weight_frequency +
                          sentenceLength * self.weight_sentence_length + sentencePosition * self.weight_sentence_position) / 4.0
            ranks[s] = totalScore
        return ranks

    def summarize(self, title, text):
        summaries = []
        sentences = utils.split_sentences(text)
        keys = self._keywords(text)
        title_words = utils.split_words(title)

        if len(sentences) <= self.ideal_sentences_nr:
            return sentences

        # score setences, and use top of them
        ranks = self._score(sentences, title_words, keys).most_common(self.ideal_sentences_nr)
        for rank in ranks:
            summaries.append(rank[0])

        return summaries
