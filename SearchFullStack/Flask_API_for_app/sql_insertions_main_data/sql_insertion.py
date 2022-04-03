import sys
import os
from sql_insertions_main_data.searchEngineFetch.gresults import get_google_results
from sql_insertions_main_data.searchEngineFetch.bing import get_bing_results
from sql_insertions_main_data.fetchAnalysis.ibm_data_sql_insertion import insert_ibm_sentiment
from sql_insertions_main_data.azure_config import azure_svname, azure_id, azure_pwd
from datetime import date, datetime
from dateutil import parser
from tqdm import tqdm
import pyodbc
from concurrent.futures import ThreadPoolExecutor

def insert_data_to_sql(results, cursor, engine, db):
    """
        For the given engine, fetch the results and store it to the database.
    """
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

def multithreading_fetch(a_kw, number_of_results, engine_name):
    """
        Create a separate connection for each result and start the insertion process.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd   
    driver= '{SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
            if engine_name == 'google':
                google_results = get_google_results(a_kw, number_of_results)
                try:
                    insert_data_to_sql(google_results, myCursor, 'google', db)
                except Exception as e:
                    print (e)
                    db.commit()
            elif engine_name == 'bing':
                bing_results = get_bing_results(a_kw, number_of_results)
                try:
                    insert_data_to_sql(bing_results, myCursor, 'bing', db)
                except:
                    db.commit()
            else:
                raise Exception("Not valid")
            db.commit()

def fetch_from_engine(engine_name, keywords_from = 'from_sql', number_of_results = 10):
    """
        Fetches the keywords from the DB or takes in the custom keywords and stats the fetching process.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd
    driver= '{SQL Server}'
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
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
                raise ValueError("The type should be string or list")
        
    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in tqdm(range(len(all_kws))):
            executor.submit(multithreading_fetch, all_kws[i], number_of_results, engine_name)
            
def add_job_schedule(list_kw, lint, nres, kwid):
    """
        Insert the data for each of the jobs into the database.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd
    driver= '{SQL Server}'
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
            query = "INSERT INTO [dbo].[jobs] (job_list, job_interval, job_results, kw_iden) VALUES (?, ?, ?, ?)"
            insertion_vals = (str(list_kw), lint, nres, kwid)
            myCursor.execute(query, insertion_vals)
            myCursor.execute("SELECT max(job_id) from [dbo].[jobs];")
            id = myCursor.fetchone()
            db.commit()
            return id
        
def get_active_schedules(kw_ident = ""):
    """
        Find the active jobs from the DB and return.
        If a kw identifier is passed, search for it and return that instead.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd
    driver= '{SQL Server}'
    print (kw_ident, '--------------------------')
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
            if kw_ident == "":
                myCursor.execute("SELECT job_id, job_list, job_interval, job_results from [dbo].[jobs] where job_status = 1;")
                res = myCursor.fetchall()
                db.commit()
                active_conn = []
                for i, j, k, l in res:
                    active_conn.append([i, j, k, l])
                return active_conn
            else:
                myCursor.execute("SELECT job_id, job_list, job_interval, job_results, job_status from [dbo].[jobs] where kw_iden = '%s';" % kw_ident)
                res = myCursor.fetchall()
                db.commit()
                active_conn = []
                for i, j, k, l, m in res:
                    active_conn.append([i, j, k, l, m])
                return active_conn
        
def del_active_schedules(iid):
    """
        Helper to delete the job from the database once the destructor is called.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd
    driver= '{SQL Server}'
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
            q = "UPDATE [dbo].[jobs] SET job_status = 0 WHERE job_id = %s" % iid
            myCursor.execute(q)
            db.commit()
            
def insert_keywords_to_db(list_kw, kw_iden):
    """
        From the React app, fetch the list of keywords and insert into the database.
    """
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd
    driver= '{SQL Server}'
    
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as db:
        with db.cursor() as myCursor:
            for kw in list_kw:
                query = "INSERT INTO [dbo].[keyword_identifier] (kw_iden, kw_name) VALUES (?, ?)"
                vals = (kw_iden, kw)
                myCursor.execute(query, vals)
            db.commit()
            
