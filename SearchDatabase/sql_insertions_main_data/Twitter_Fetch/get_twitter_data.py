from sql_insertions_main_data.Twitter_Fetch.twitter_config import consumer_key, consumer_secret, access_token, access_token_secret
from sql_insertions_main_data.fetchAnalysis.local_ibm import ibm_get_sentiment_twitter
from sql_insertions_main_data.azure_config import azure_svname, azure_id, azure_pwd

from tqdm import tqdm
import tweepy
import pyodbc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

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
        "INSERT INTO [search_analysis].[twitter_sentiment] "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    cursor.execute(query, query_insertion)
    

def insert_twitter_sql(results, cursor, db, kw):
    for result in results:
        tweet_id = str(result.id)
        created_at = result.created_at
        text = result.full_text
        url = 'https://twitter.com/twitter/statuses/%s'%tweet_id
        keyword_query = kw
        favorite_count = result.favorite_count
        retweet_count = result.retweet_count
        # cursor.execute("SELECT id from [search_analysis].[twitter_sentiment] WHERE id = %s" %tweet_id)
        cursor.execute("SELECT tweet_id FROM [search_analysis].[tweets] WHERE tweet_id = %s" %tweet_id)
        tweet_res = cursor.fetchone()
        if not tweet_res:
            insert_ibm_twitter(text, url, keyword_query, tweet_id, cursor)
            query = "INSERT INTO [search_analysis].[tweets] VALUES  (?, ?, ?, ?, ?, ?, ?, ?)"
            now = datetime.now()
            insertion_vals = (tweet_id, text, created_at, favorite_count, retweet_count, keyword_query, url, now)
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

def twitter_multithreading(a_kw, number_of_results, db):
    with db.cursor() as myCursor:
        all_twitter_results = get_twitter(a_kw, number_of_results)
        try:
            insert_twitter_sql(all_twitter_results, myCursor, db, a_kw)
        except Exception as e:
            print (e)
            print ("Failed to fetch tweet.")
            db.commit()
        db.commit()

def fetch_from_twitter(keywords_from = 'from_sql', number_of_results = 10):
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd  
    driver= '{ODBC Driver 17 for SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password+';MARS_Connection=yes;') as db:
        with db.cursor() as myCursor:
            if keywords_from == 'from_sql':
                myCursor.execute("SELECT kw_name FROM [search_analysis].[keywords]")
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
        
        with ThreadPoolExecutor(max_workers=len(all_kws)) as executor: 
            for i in tqdm(range(len(all_kws))):
                executor.submit(twitter_multithreading, all_kws[i], number_of_results, db)