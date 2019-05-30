import re


def split_words(text):
    # split a string into array of words
    try:
        text = re.sub(r'[^\w ]', '', text, flags=re.UNICODE)
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        print("Error while splitting characters")
        return None


def split_sentences(text):
    '''
    The regular expression matches all sentence ending punctuation and splits the string at those points.
    At this point in the code, the list looks like this ["Hello, world", "!" ... ]. The punctuation and all quotation marks
    are separated from the actual text. The first s_iter line turns each group of two items in the list into a tuple,
    excluding the last item in the list (the last item in the list does not need to have this performed on it). Then,
    the second s_iter line combines each tuple in the list into a single item and removes any whitespace at the beginning
    of the line. Now, the s_iter list is formatted correctly but it is missing the last item of the sentences list. The
    second to last line adds this item to the s_iter list and the last line returns the full list.
    '''
    sentences = re.split('(?<![A-ZА-ЯЁ])([.!?]"?)(?=\s+\"?[A-ZА-ЯЁ])', text, flags=re.UNICODE)
    s_iter = list(zip(*[iter(sentences[:-1])] * 2))
    s_iter = [''.join(map(str, y)).lstrip() for y in s_iter]
    s_iter.append(sentences[-1])
    return s_iter
