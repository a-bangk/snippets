import sys
import mariadb
from sqlalchemy import create_engine, text
import pymysql
from snippets import settings 

def get_db_connection():
    try: 
        conn = mariadb.connect( 
            user=settings.MYSQL.auth.USER, 
            password=settings.MYSQL.auth.get('passwd'), 
            host=settings.MYSQL.host, 
            port=settings.MYSQL.port, 
            database=settings.MYSQL.database 
        ) 

    except mariadb.Error as e: 
            print(f"Error connecting to MariaDB Platform: {e}") 
            sys.exit(1) 
    return conn 

def commaStringToList(commaString):
    itemList=commaString.split(',')
    itemList = [item.strip() for item in itemList]
    while("" in itemList):
        itemList.remove("")
    itemList = sorted(itemList, key=str.casefold)
    return itemList

def conn_alchemy():
    engine = create_engine('mysql+pymysql://'+settings.MYSQL.auth.USER+':'+settings.MYSQL.auth.get("passwd")+'@'+settings.MYSQL.host+':'+str(settings.MYSQL.port)+'/'+settings.MYSQL.database, pool_recycle=3600, echo=True)
    return engine.connect()
     
#result=conn_alchemy().execute(text('select * from note;'))
#print(result.fetchall())