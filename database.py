import os 
import mysql.connector 
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

dbPool = pooling.MySQLConnectionPool(
    pool_name = "moviePool",
    pool_size = 5,
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASS"),
    database = os.getenv("DB_NAME"), 
)

def get_db_connection():
    return dbPool.get_connection()
    