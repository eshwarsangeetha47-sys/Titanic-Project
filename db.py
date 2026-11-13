

import os
import psycopg2
import pandas as pd

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="titanic_db",
        user="postgres",
        password=os.getenv("PGPASSWORD"),
        port="5432"
    )
    return conn

def get_data():
    conn = get_connection()

    query = """
    SELECT *
    FROM titanic_project.passengers
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df

