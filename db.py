import streamlit as st
import psycopg2
import pandas as pd

def get_connection():
    conn = psycopg2.connect(
        st.secrets["DATABASE_URL"]
    )
    return conn

def get_data():
    conn = get_connection()

    query = """
    SELECT *
    FROM passengers
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df