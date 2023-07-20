import re

from nltk.corpus import stopwords
from string import punctuation

stopwords = set(stopwords.words('english'))
punctuation = list(punctuation)


def remove_stop_words(text):
    return [cleanse(word) for word in text.split() if not is_filler_word(word.lower())]


def is_filler_word(word):
    cleansed_word = cleanse(word)
    return cleansed_word in stopwords or cleansed_word in punctuation or len(cleansed_word) <= 3


def cleanse(word):
    new_text = re.sub(r"[^a-zA-Z0-9 ]", "", word)
    return new_text.lower()
