from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions, CategoriesOptions, EmotionOptions
import json
from newspaper import Article

def get_text_from_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def ibm_get_sentiment(url, keyword):
    print (keyword)
    url_api = 'aEgAo9_wTdLPk1gklVeKHukDzkXp5gXote0yttpMPrC0'
    url_ibm = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/7fade06f-33fa-4aa6-8e0d-64acca721fa4'

    ibm_authenticator = IAMAuthenticator(url_api)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25', authenticator=ibm_authenticator)
    natural_language_understanding.set_service_url(url_ibm)
    try:
        response = natural_language_understanding.analyze(
            url=url,
            features=Features(
                categories=CategoriesOptions(limit=3),
                emotion=EmotionOptions(),
                sentiment=SentimentOptions(),
                keywords = KeywordsOptions(sentiment = True, limit = 5),
                entities= EntitiesOptions(sentiment = True, limit = 3)
                )).get_result()
        if response['sentiment']['document']['score'] == 0:
            raise Exception("TRY FETCHING")

    except Exception as e:
        print ("TRYING DIRECT FETCH")
        try:
            response = natural_language_understanding.analyze(
                text = get_text_from_url(url),
                features=Features(
                    categories=CategoriesOptions(limit=3),
                    emotion=EmotionOptions(),
                    sentiment=SentimentOptions(),
                    keywords = KeywordsOptions(sentiment = True, limit = 5),
                    entities= EntitiesOptions(sentiment = True, limit = 3)
                    )).get_result()
        except:
            print ("FETCH FAILED: RETURING DEFAULTS")
            response =  {
                'usage': {
                    'text_characters': 0
                },
                'sentiment': {},
                'emotion': {},
            }
    return response