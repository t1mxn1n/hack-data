# -*- coding: utf8 -*-
import pickle
import string
import nltk

nltk.download('punkt')
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

russian_stop_words = stopwords.words('russian')
snowball = SnowballStemmer(language='russian')

main_dataset = pd.read_csv('dataset/dataset.csv')


def tokenize_sentence(sentence):
    tokens = word_tokenize(sentence, language='russian')
    tokens = [i for i in tokens if i not in string.punctuation]
    tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens


def tokenize(x):
    return tokenize_sentence(x)


def modeling():
    train_df, test_df = train_test_split(
        main_dataset, test_size=500
    )

    model_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=tokenize_sentence)),
        ('model', LogisticRegression(random_state=0))
    ])

    model_pipeline.fit(train_df['discussion'], train_df['role'])

    filename = 'model_v1.pk'
    with open(filename, 'wb') as file:
        pickle.dump(model_pipeline, file)


if __name__ == '__main__':
    modeling()
