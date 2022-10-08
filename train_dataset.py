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

    main_csv = pd.read_csv('dataset.csv')
    train_df, test_df = train_test_split(
        main_csv, test_size=500
    )

    # vectorizer = TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, rm_stop_words=True))
    # features = vectorizer.fit_transform(train_df['comment'])

    # model = LogisticRegression(random_state=0).fit(features, train_df['toxic'])


    model_pipeline = Pipeline([
        ('vectorizer', TfidfVectorizer(tokenizer=lambda x: tokenize_sentence(x, rm_stop_words=True))),
        ('model',  LogisticRegression(random_state=0))
    ])
    model_pipeline.fit(train_df['discussion'], train_df['role'])
    print(model_pipeline.predict(['Саудовская Аравия не использует нефть в качестве оружия, заявил государственный министр по иностранным делам Саудовской Аравии Адель аль-Джубейр. Он назвал неверной мысль о том, что Эр-Рияд сокращает добычу вместе с ОПЕК+ для того, чтобы навредить США. «Нефть — это не оружие. Это не истребитель. Это не танк. Из нее нельзя стрелять. Мы рассматриваем нефть как товар и как важную часть мировой экономики… Идея о том, что Саудовская Аравия делает это, чтобы навредить США или из политической вовлеченности, в корне неверна»,— сказал министр Fox News.Эр-Рияд утверждает, что ОПЕК+ сокращает добычу нефти в качестве упреждающей меры, чтобы не допустить краха энергетического рынка. По словам министра, Саудовская Аравия хочет сохранить стабильность на рынке нефти в интересах стран-производителей и стран-покупателей.Государства—участники ОПЕК+ ранее на этой неделе согласились на сокращение добычи нефти на 2 млн баррелей в сутки. Это самое большое сокращение с 2020 года. Президент США Джо Байден назвал решение близоруким, США готовят на него ответ. ']))
    print(model_pipeline.predict(['Президент России Владимир Путин поручил правительству создать российского оператора проекта «Сахалин-1». Как следует из указа главы государства, организации будут переданы все права и обязанности действующего оператора Exxon Neftegas Limited.Доли в уставном капитале нового проекта будут разделены между дочерними компаниями «Роснефти», которые участвуют в проекте. АО «Сахалинморнефтегаз-Шельф» получит 11,5%, «РИ-Астра» — 8,5%. Остальные 80% передадут новому оператору до тех пор, пока все доли не будут распределены. Иностранные участники «Сахалина-1» в течение месяца должны подтвердить согласие принять в собственность пропорциональную долю в новом операторе. Долями в проекте владели американская ExxonMobil (30%), японская Sodeco (30%) и индийская ONGC (20%).Согласно указу, новый оператор «Сахалина-1» и его участники сохранят специальный налоговый режим, таможенное, таможенно-тарифное регулирование, а также исключительное право на экспорт газа.В июне похожая схема перевода в российскую юрисдикцию была применена к «Сахалину-2». Вместо Sakhalin Energy им стала созданная в России структура «Сахалинская энергия». Россия также одобрила участие в проекте японских компаний Mitsubishi и Mitsui (они получили по 10% и 12,5% соответственно).В конце сентября губернатор Сахалинской области Валерий Лимаренко сообщил, что объем добычи нефти и конденсата на «Сахалине-1» за семь месяцев уменьшился почти вдвое по сравнению с аналогичным периодом 2021 года.В июле российские власти заявили, что добыча на проекте «Сахалин-1» «из-за введенных ограничений» сократилась в 22 раза — с 220 тыс. до 10 тыс. баррелей в сутки. Резкое снижение объемов добываемой нефти произошло после того, как оператор «Сахалина-1» ExxonMobil заявила о прекращении участия и отозвала своих специалистов. Минэнерго считает, что добыча на «Сахалине-1» была остановлена под надуманным предлогом. ']))
    print(model_pipeline.predict(['С конца февраля иностранные компании, ограничившие свою деятельность или заявившие об уходе с российского рынка, потеряли от $200 млрд до $240 млрд, подсчитали эксперты Центра стратегических разработок. Наибольшие потери в стоимостном выражении понес бизнес из США, Великобритании и Германии. Всего по состоянию на 9 сентября 2022 года 7% крупнейших иностранных компаний, работавших в России, заявили о полном уходе с отечественного рынка. Еще 34% ограничили свою деятельность, 15% решили покинуть страну через передачу новому собственнику российского подразделения. По подсчетам ЦСР, всего в России работало около 600 крупнейших компаний, на которые приходилось до 1 млн рабочих мест.']))
    print(model_pipeline.predict(['В России с января по сентябрь было продано 753,5 тыс. новых автомобилей и легких коммерческих автомобилей, сообщила Ассоциация европейского бизнеса (.pdf). Это на 59,6% меньше, чем за аналогичный период 2021 года.В сентябре динамика спада немного замедлилась. За месяц продажи составили 46,7 тыс., что на 59,6% меньше, чем в сентябре 2021 года. В августе продажи автомобилей и легких коммерческих автомобилей снизились на 62,4% по сравнению с аналогичным периодом 2021 года (41,7 тыс.).']))
    print(model_pipeline.predict(['бизнес']))
    print(model_pipeline.predict(['финансы']))
    print(model_pipeline.predict(['деньги']))
    print(model_pipeline.predict(['бухгалтерия']))
    print(model_pipeline.predict(['3 ндфл']))
    print(model_pipeline.predict(['денис никита тимофей']))
    print(model_pipeline.predict(['говно']))
    # Save the vectorizer
    # vec_file = 'vectorizer.pickle'
    # pickle.dump(TfidfVectorizer(), open(vec_file, 'wb'))
    #
    # # Save the model
    # mod_file = 'classification.model'
    # joblib.dump(model_pipeline, mod_file)
    filename = 'model_v1.pk'
    with open(filename, 'wb') as file:
        pickle.dump(model_pipeline, file)


if __name__ == '__main__':
    modeling()
