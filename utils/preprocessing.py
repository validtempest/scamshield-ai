import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english') + stopwords.words('indonesian'))


def preprocess_text(text):

    # lowercase
    text = text.lower()

    # hapus url
    text = re.sub(r'http\S+', '', text)

    # hapus karakter aneh
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # tokenization
    tokens = word_tokenize(text)

    # hapus stopwords
    filtered_tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    # gabung lagi jadi string
    cleaned_text = " ".join(filtered_tokens)

    return cleaned_text