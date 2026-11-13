
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_data, get_connection

st.set_page_config(page_title="Titanic Dashboard", layout="wide")

st.title("🚢 Titanic Dataset Dashboard")
# Database Connection Status
try:
    conn = get_connection()
    conn.close()
    st.success("🟢 Database Connected Successfully!")
except Exception as e:
    st.error("🔴 Database Connection Failed!")
    st.error(str(e))
    st.stop()
st.write("Analysis of Titanic passenger records")

# Load data from PostgreSQL
df = get_data()

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Passengers", len(df))
col2.metric("Survived", int(df["survived"].sum()))
col3.metric("Did Not Survive", int((df["survived"] == 0).sum()))

st.divider()

# Sidebar filter
st.sidebar.header("Passenger Filter")

selected_class = st.sidebar.selectbox(
    "Select Passenger Class",
    ["All", 1, 2, 3]
)

if selected_class == "All":
    filtered_df = df
else:
    filtered_df = df[df["pclass"] == selected_class]

# Passenger details
st.subheader("Passenger Details")
st.dataframe(filtered_df, use_container_width=True)

# Survival chart
st.subheader("Survival Analysis")

survival_count = filtered_df["survived"].value_counts().sort_index()

fig, ax = plt.subplots()
ax.bar(["Not Survived", "Survived"], [
    survival_count.get(0, 0),
    survival_count.get(1, 0)
])
ax.set_ylabel("Number of Passengers")
ax.set_title("Passenger Survival")
st.pyplot(fig)

# Gender analysis
st.subheader("Survival by Gender")

gender_data = filtered_df.groupby("sex")["survived"].sum()

st.bar_chart(gender_data)

# Age analysis
st.subheader("Passenger Age Distribution")

st.bar_chart(filtered_df["age"].dropna().value_counts().sort_index())

st.success("Titanic Dashboard Loaded Successfully!")
