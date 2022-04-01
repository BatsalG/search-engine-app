from sql_insertions_main_data.Twitter_Fetch.twitter_config import consumer_key, consumer_secret, access_token, access_token_secret
from numpy import result_type
from sql_insertions_main_data.fetchAnalysis.local_ibm import ibm_get_sentiment_twitter
from tqdm import tqdm
import tweepy
import mysql.connector


def insert_ibm_twitter(text, url, kw, tweet_id, cursor):
    query_insertion = []
    res = ibm_get_sentiment_twitter(text)

    query_insertion.append(str(tweet_id))
    query_insertion.append(res['usage']['text_characters'])
    query_insertion.append(url)
    query_insertion.append(kw)
    
    if 'document' in res['sentiment']:
        query_insertion.append(res['sentiment']['document']['score'])
        query_insertion.append(res['sentiment']['document']['label'])
    else:
        query_insertion.append(None)
        query_insertion.append(None)
    
    if 'document' in res['emotion']:
        query_insertion.append(res['emotion']['document']['emotion']['sadness'])
        query_insertion.append(res['emotion']['document']['emotion']['joy'])
        query_insertion.append(res['emotion']['document']['emotion']['anger'])
        query_insertion.append(res['emotion']['document']['emotion']['disgust'])
        query_insertion.append(res['emotion']['document']['emotion']['fear'])
    else:
        for i in range(5):
            query_insertion.append(None)
    
    if 'keywords' in res and res['keywords']:
        query_insertion.append((res['keywords'])[0]['text'])
        query_insertion.append((res['keywords'])[0]['sentiment']['score'])
        query_insertion.append((res['keywords'])[0]['relevance'])
    else:
        query_insertion.append(None)
        query_insertion.append(None)
        query_insertion.append(None)

    if 'entities' in res and res['entities']:
        query_insertion.append((res['entities'])[0]['type'])    
        query_insertion.append((res['entities'])[0]['text'])    
        query_insertion.append((res['entities'])[0]['sentiment']['score'])    
        query_insertion.append((res['entities'])[0]['relevance'])
    else:
        for _ in range(4):
            query_insertion.append(None)
    query = (
        "INSERT INTO twitter_sentiment "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(query, query_insertion)
    

def insert_twitter_sql(results, cursor, db, kw):
    for result in results:
        tweet_id = result.id
        created_at = result.created_at
        text = result.full_text
        url = 'https://twitter.com/twitter/statuses/%s'%tweet_id
        keyword_query = kw
        favorite_count = result.favorite_count
        retweet_count = result.retweet_count
        cursor.execute("SELECT tweet_id FROM tweets WHERE tweet_id = %s" %str(tweet_id))
        tweet_res = cursor.fetchone()
        if tweet_res:
            continue
        insert_ibm_twitter(text, url, keyword_query, tweet_id, cursor)
        query = "INSERT IGNORE INTO tweets VALUES  (%s, %s, %s, %s, %s, %s, %s)"
        insertion_vals = (tweet_id, text, created_at, favorite_count, retweet_count, keyword_query, url)
        cursor.execute(query, insertion_vals)
        db.commit()

def get_twitter(kw, number_of_results):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, )
    
    res = api.search_tweets(
        q = kw,
        lang = 'en',
        result_type = 'popular',
        count = number_of_results,
        tweet_mode = "extended"
    )
    return res

def fetch_from_twitter(keywords_from = 'from_sql', number_of_results = 10):
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "4310",
        database = "search_analysis"
    )
    myCursor = db.cursor()
    
    if keywords_from == 'from_sql':
        myCursor.execute("SELECT kw_name FROM keywords")
        kws_cursor = myCursor.fetchall()
        all_kws = [i[0] for i in kws_cursor]
    elif type(keywords_from) is str:
        all_kws = [keywords_from]
    elif type(keywords_from) is list:
        if len(keywords_from) == 0:
            raise Exception("The list is empty.")
        all_kws = keywords_from
    else:
        return "Not Found Any Keyword"
        
    for i in tqdm(range(len(all_kws))):
        all_twitter_results = get_twitter(all_kws[i], number_of_results)
        try:
            insert_twitter_sql(all_twitter_results, myCursor, db, all_kws[i])
        except Exception as e:
            print (e)
            print ("Failed to fetch tweet.")
            db.commit()
    db.commit()
    
