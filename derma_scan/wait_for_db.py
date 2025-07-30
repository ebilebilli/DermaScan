import time
import sys
import psycopg2
from psycopg2 import OperationalError
import os

def wait_for_db():
    db_host = os.getenv('POSTGRES_HOST', 'db')
    db_port = os.getenv('POSTGRES_PORT', 5432)
    db_name = os.getenv('POSTGRES_DB')
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')

    while True:
        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password
            )
            conn.close()
            print("Database is ready!")
            break
        except OperationalError:
            print("Database is unavailable, waiting 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    wait_for_db()
