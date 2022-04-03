import mysql.connector
import pyodbc
from sql_insertions_main_data.azure_config import azure_pwd, azure_id, azure_svname

def create_table_keyword(cursor):
    cursor.execute("""
                   CREATE TABLE keywords
                    (kw_id int NOT NULL IDENTITY(1,1) PRIMARY KEY,
                    kw_name varchar(255) NOT NULL );
                   """
    )
    

def create_table(tab_name):
    server = azure_svname
    database = 'search_analysis'
    username = azure_id
    password = azure_pwd  
    driver= '{SQL Server}'

    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            create_table_keyword(cursor)



if __name__ == '__main__':
    create_table('keywords')