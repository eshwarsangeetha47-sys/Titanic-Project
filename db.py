
import os
import streamlit as st
import psycopg2
import pandas as pd


def get_database_url():
    url = os.getenv("DATABASE_URL")

    if not url:
        try:
            url = st.secrets["DATABASE_URL"]
        except Exception:
            url = None

    return url


def get_connection():
    database_url = get_database_url()

    # Online database connection (Neon)
    if database_url:
        conn = psycopg2.connect(
            database_url,
            sslmode="require"
        )
    else:
        # Local database connection (pgAdmin)
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

    if get_database_url():
        query = """
        SELECT *
        FROM public.passengers
        """
    else:
        query = """
        SELECT *
        FROM titanic_project.passengers
        """

    df = pd.read_sql(query, conn)
    conn.close()

    return df
