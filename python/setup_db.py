import os
from dotenv import load_dotenv
import psycopg2

load_dotenv('python/.env')

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

with open('python/init.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

try:
    con = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = con.cursor()
    cursor.execute(sql_content)
    con.commit()
    cursor.close()
    con.close()
    print("✓ Database initialized successfully!")
except Exception as e:
    print(f"✗ Error: {e}")