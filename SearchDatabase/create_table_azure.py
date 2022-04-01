import mysql.connector
import pyodbc

def create_table_keyword(cursor):
    cursor.execute("""
                   CREATE TABLE keywords
                    (kw_id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
                    kw_name varchar(255) NOT NULL );
                   """
    )
    

def create_table(tab_name):
    server = 'capstone-search.database.windows.net'
    database = 'search_analysis'
    username = 'batsalg'
    password = '{Mangoman123}'   
    driver= '{SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            create_table_keyword(cursor)

    # db = mysql.connector.connect(
    #     host = "capstone-search.database.windows.net",
    #     user = "batsalg@capstone-search",
    #     password = "Mangoman123",
    #     port = 1433,
    #     database = "search_analysis",
    #     client_flags = [mysql.connector.ClientFlag.SSL],
    #     ssl_ca = './DigiCertGlobalRootG2.crt.pem'
    # )
    # myCursor = db.cursor()
    # if tab_name == 'keywords':
    #     create_table_keyword(myCursor)
    # elif tab_name == 'news':
    #     create_table_news(myCursor)
    # elif tab_name == 'news_sentiment':
    #     create_table_news_sentiment(myCursor)
    # elif tab_name == 'tweets':
    #     create_table_tweets(myCursor)
    # elif tab_name  == 'twitter_sentiment':
    #     create_table_twitter_sentiment(myCursor)
    # else:
    #     raise Exception("Invalid Table Creation Requested")



if __name__ == '__main__':
    create_table('keywords')