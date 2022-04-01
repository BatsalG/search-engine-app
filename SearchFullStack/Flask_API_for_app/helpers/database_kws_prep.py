import mysql.connector
import csv

def get_kw_list(fileName):
    try:
        kw_file = open(fileName, 'r')
        csv_reader = csv.reader(kw_file)
        kws = []
        for kw in csv_reader:
            kws.append([kw[0]])
    except:
        return "ERROR: Couldn't load CSV file."
    else:
        kw_file.close()
    print (kws)
    return kws

def insert_kws_to_sql(list_kws):
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "4310",
        database = "search_analysis"
    )
    myCursor = db.cursor()
    sql_insertion = "INSERT INTO keywords (kw_name) VALUES (%s)"
    myCursor.executemany(sql_insertion, list_kws)
    db.commit()
    return "Successfully added the keywords."

def not_needed():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "4310",
        database = "search_analysis"
    )
    myCursor = db.cursor()
    myCursor.execute('''
                     CREATE TABLE tweets (
                         tweet_id INT NOT NULL PRIMARY KEY,
                         tweet_data TEXT NOT NULL,
                         created_at DATE,
                         favorite_count INT,
                         retweet_count INT,
                         keyword_query VARCHAR(1000)
                    )''')

    myCursor.execute('''
                     CREATE TABLE keywords (
                         kw_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                         kw_name VARCHAR(255) NOT NULL
                     )
                     ''')