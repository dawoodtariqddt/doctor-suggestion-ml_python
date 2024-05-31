#app/database.py
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        user='root',
        password='12345678',
        host='localhost',
        database='careaid'
    )
    return conn
