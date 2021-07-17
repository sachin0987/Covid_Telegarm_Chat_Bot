import json
import requests
import time
import urllib
from sqlalchemy import create_engine
import pandas as pd
import re
from datetime import datetime
import mysql.connector
dbname="telegram_db"

def db_connection2():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sachin",
    database="telegram_db"
    )
    mycursor = mydb.cursor()
    return mycursor

def db_connection(dbname):
    try:
        engine = create_engine(f"mysql+pymysql://root:sachin@localhost/{dbname}")
        db_conn = engine.connect()
    except Exception as err:
        print(err)
        db_conn=False
    finally:
        return db_conn

def get_info_from_db(dbname,tablename,city):
    city=(city.lower())[0:3]
    print(city)
    try:
        con=db_connection(dbname)
        df = pd.read_sql_query(f"select * from {tablename} WHERE city Like '{city}%'", con)
        # print(df)
        # print(df.empty )
        if df.empty != True :
            dict_list=(df.T.to_dict().values())
            return dict_list
        else:
            return None
    except Exception as err:
        print(err)

def write_data_to_db(tablename,city,cat_message,msg):
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sachin",
        database="telegram_db"
        )
        mycursor = mydb.cursor()
        city=city.lower()
        query=f'''UPDATE covid_help2 SET {cat_message} ='{msg}' WHERE {cat_message} is NULL and city LIKE '%{city}%';'''      
        #sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        if mycursor.rowcount == 0:
            # query=f'''SELECT {city},{cat_message} from {tablename} WHERE {cat_message}='{msg}';'''
            # print(query)
            # mycursor.execute(query)
            # print(mycursor)

            query=(f'''INSERT IGNORE INTO {tablename} (city,{cat_message}) values ('{city}','{msg}');''')
            mycursor.execute(query)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")
            # check_duplicate_and_remove('covid_help2',city,cat_message)

        #     INSERT INTO TABLE_2(id, name) SELECT t1.id,t1.name FROM TABLE_1 t1 WHERE NOT EXISTS(SELECT id FROM TABLE_2 t2 WHERE t2.id = t1.id)
        # print(city,cat_message)
        # engine=db_connection(dbname)
        # # query=f'''SELECT * from {tablename} WHERE city={city} and {cat_message} IS NULL;'''
        # # print(query)
        # # status =engine.execute(query)
        # # print(status)
        # query=f'''UPDATE covid_help2 SET {cat_message} ='{msg}' WHERE {cat_message} is NULL and city LIKE '%{city}%';'''
        # print(query)
        # status =engine.execute(query)
        # print(status,".....................................printing Status")
        # # query=(f'''INSERT into {tablename} (city,{cat_message}) values ('{city}','{msg}');''')
        # # status =engine.execute(query)
        # # print(status)
        # print('''""""""""Updated """""""""""""""""""''')
    except:
        pass

# def check_duplicate_and_remove(tablename,city,cat_message):

#     try:
#         con=db_connection(dbname)
#         df = pd.read_sql_query(f"select * from {tablename}", con)
#         print(df)
#         df = df.drop_duplicates(subset = [city,cat_message], keep = 'first')
#         print(df)
#     except:
#         pass

if __name__ == '__main__':
   
    pass
    # dbname="telegram_db"
    # # get_info_from_db(dbname,"covid_help",'Delhi')
    # check=get_messages('Pune','A')
    # print(check)
