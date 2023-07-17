import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords

def filter_stopwords(text):
    stopwords = set(stopwords.words('english'))
    filtered_text = ' '.join(word for word in text.split() if word.lower() not in stopwords)
    return filtered_text
