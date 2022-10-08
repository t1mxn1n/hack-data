import pickle
import string
import joblib

import nltk
nltk.download('punkt')
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

russian_stop_words = stopwords.words('russian')
snowball = SnowballStemmer(language='russian')


def tokenize_sentence(sentence, rm_stop_words=True):
    tokens = word_tokenize(sentence, language='russian')
    tokens = [i for i in tokens if i not in string.punctuation]
    if rm_stop_words:
        tokens = [i for i in tokens if i not in russian_stop_words]
    tokens = [snowball.stem(i) for i in tokens]
    return tokens


def modeling():

    main_csv = pd.read_csv('toxic_comments.csv')
    main_csv['toxic'] = main_csv['toxic'].apply(int)
    train_df, test_df = train_test_split(
        main_csv, test_size=500
    )
    example = main_csv.iloc[1]['comment']
    # print(tokenize_sentence(example))

    # ref_comment = pd.read_csv('toxic_comments_ref.csv')['comment']
    # ref_toxic = pd.read_csv('toxic_comments_ref.csv')['toxic']
    # main_comment, main_toxic, comment_list, toxic_list = list(), list(), list(), list()
    # for comment in main_csv['comment']:
    #     main_comment.append(comment.replace('\n', ''))
    # for toxic in main_csv['toxic']:
    #     main_toxic.append(int(toxic))
    # for comment in ref_comment:
    #     comment_list.append(comment)
    # for toxicity in ref_toxic:
    #     toxic_list.append(toxicity)
    # vect = CountVectorizer(token_pattern=r'\b\w+\b').fit(comment_list)
    # print(vect.get_feature_names())

    # train_df, test_df = train_test_split(
    #     main_csv
    # )

    vectorizer = TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, rm_stop_words=True))
    features = vectorizer.fit_transform(train_df['comment'])
    # print(features)

    model = LogisticRegression(random_state=0).fit(features, train_df['toxic'])
    # print(model.predict(features[0]))
    model_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, rm_stop_words=True))),
        ('model',  LogisticRegression(random_state=0))
    ])
    model_pipeline.fit(train_df['digest'], train_df['category'])
    print(model_pipeline.predict(['У меня всё хорошо']))
    print(model_pipeline.predict(['Я бы такое смотреть не стал']))
    print(model_pipeline.predict(['Лютый отстой']))
    print(model_pipeline.predict(['Лучше говна в жизни не видел']))
    # Save the vectorizer
    vec_file = 'vectorizer.pickle'
    pickle.dump(TfidfVectorizer(), open(vec_file, 'wb'))

    # Save the model
    mod_file = 'classification.model'
    joblib.dump(model_pipeline, mod_file)


if __name__ == '__main__':
    modeling()
