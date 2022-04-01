import sys
import os
from sql_insertions_main_data.searchEngineFetch.gresults import get_google_results
from sql_insertions_main_data.searchEngineFetch.bing import get_bing_results
from sql_insertions_main_data.fetchAnalysis.ibm_data_sql_insertion import insert_ibm_sentiment
from sql_insertions_main_data.azure_config import azure_svname, azure_id, azure_pwd

from datetime import date, datetime
from dateutil import parser
from tqdm import tqdm
import mysql.connector
import pyodbc


def insert_data_to_sql(results, cursor, engine, db):
    for res in results:
        date_ref = parser.parse(res['published_date'])
        url, kw = res['url'], res['keyword']
        cursor.execute("SELECT id FROM [search_analysis].[news_sentiment] WHERE url = '%s';" % url)
        sent_res = cursor.fetchone()
        if not sent_res:
            sent_id = insert_ibm_sentiment(url, kw, cursor)
        else:
            sent_id = sent_res[0]
        query = "INSERT INTO [search_analysis].[news] (keyword, search_engine, published_date, news_title, news_url, publisher_name, publisher_description, sentiment_id) VALUES  (?, ?, ?, ?, ?, ?, ?, ?)"
        insertion_vals = (res['keyword'], engine, date_ref, res['title'], res['url'], res['publisher'], res['description'], sent_id)
        cursor.execute(query, insertion_vals)
        db.commit()

def fetch_from_engine(keywords_from = 'from_sql', number_of_results = 10):
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd   
    driver= '{SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
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
                raise ValueError("The type should be string or list")
            
            for i in tqdm(range(len(all_kws))):
                google_results = get_google_results(all_kws[i], number_of_results)
                try:
                    insert_data_to_sql(google_results, myCursor, 'google', db)
                except Exception as e:
                    print (e)
                    db.commit()
                bing_results = get_bing_results(all_kws[i], number_of_results)
                try:
                    insert_data_to_sql(bing_results, myCursor, 'bing', db)
                except:
                    db.commit()
        
            db.commit()
    