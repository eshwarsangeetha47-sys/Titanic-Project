
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_data, get_connection

st.set_page_config(
    page_title="Titanic Dashboard",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 Titanic Passenger Dashboard")
st.write("Complete analysis of Titanic passenger records")

# Database connection
try:
    conn = get_connection()
    conn.close()
    st.success("🟢 Database Connected Successfully!")
except Exception as e:
    st.error("🔴 Database Connection Failed!")
    st.error(str(e))
    st.stop()

# Load data
try:
    df = get_data()
except Exception as e:
    st.error("Unable to load passenger data.")
    st.error(str(e))
    st.stop()

if df.empty:
    st.warning("No passenger records found.")
    st.stop()

# Prepare data
df["survived"] = pd.to_numeric(df["survived"], errors="coerce")
df["pclass"] = pd.to_numeric(df["pclass"], errors="coerce")
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["fare"] = pd.to_numeric(df["fare"], errors="coerce")

# Sidebar filters
st.sidebar.header("🔎 Passenger Filters")

classes = sorted(df["pclass"].dropna().unique().tolist())

selected_class = st.sidebar.selectbox(
    "Passenger Class",
    ["All"] + classes
)

genders = sorted(df["sex"].dropna().unique().tolist())

selected_gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + genders
)

ports = sorted(df["embarked"].dropna().unique().tolist())

selected_port = st.sidebar.selectbox(
    "Embarkation Port",
    ["All"] + ports
)

filtered_df = df.copy()

if selected_class != "All":
    filtered_df = filtered_df[
        filtered_df["pclass"] == selected_class
    ]

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["sex"] == selected_gender
    ]

if selected_port != "All":
    filtered_df = filtered_df[
        filtered_df["embarked"] == selected_port
    ]

# KPI calculations
total = len(filtered_df)
survived = int(filtered_df["survived"].eq(1).sum())
not_survived = int(filtered_df["survived"].eq(0).sum())

survival_rate = (
    survived / total * 100 if total > 0 else 0
)

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Passengers", total)
col2.metric("Survived", survived)
col3.metric("Deaths", not_survived)
col4.metric("Survival Rate", f"{survival_rate:.1f}%")

st.divider()

# Survival distribution
st.subheader("1. Survival Distribution")

col1, col2 = st.columns(2)

with col1:
    survival_counts = filtered_df["survived"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        [survival_counts.get(1, 0), survival_counts.get(0, 0)],
        labels=["Survived", "Did Not Survive"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("Passenger Survival Percentage")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig, ax = plt.subplots()

    ax.bar(
        ["Survived", "Did Not Survive"],
        [survived, not_survived]
    )

    ax.set_title("Survival Count")
    ax.set_ylabel("Number of Passengers")

    st.pyplot(fig)
    plt.close(fig)

st.divider()

# Survival by gender
st.subheader("2. Survival by Gender")

gender_data = filtered_df.groupby(
    ["sex", "survived"]
).size().unstack(fill_value=0)

fig, ax = plt.subplots()

gender_data.rename(
    columns={0: "Did Not Survive", 1: "Survived"}
).plot(kind="bar", ax=ax)

ax.set_title("Survival by Gender")
ax.set_xlabel("Gender")
ax.set_ylabel("Number of Passengers")
ax.legend(title="Result")
ax.tick_params(axis="x", rotation=0)

st.pyplot(fig)
plt.close(fig)

st.divider()

# Survival by passenger class
st.subheader("3. Survival by Passenger Class")

class_data = filtered_df.groupby(
    ["pclass", "survived"]
).size().unstack(fill_value=0)

fig, ax = plt.subplots()

class_data.rename(
    columns={0: "Did Not Survive", 1: "Survived"}
).plot(kind="bar", ax=ax)

ax.set_title("Passenger Class Survival")
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Number of Passengers")
ax.legend(title="Result")
ax.tick_params(axis="x", rotation=0)

st.pyplot(fig)
plt.close(fig)

st.divider()

# Age distribution
st.subheader("4. Passenger Age Distribution")

age_data = filtered_df["age"].dropna()

fig, ax = plt.subplots()

ax.hist(age_data, bins=20, edgecolor="black")
ax.set_title("Age Distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Number of Passengers")

st.pyplot(fig)
plt.close(fig)

st.divider()

# Average fare by class
st.subheader("5. Average Fare by Passenger Class")

fare_data = filtered_df.groupby("pclass")["fare"].mean()

fig, ax = plt.subplots()

ax.bar(
    fare_data.index.astype(str),
    fare_data.values
)

ax.set_title("Average Fare by Class")
ax.set_xlabel("Passenger Class")
ax.set_ylabel("Average Fare")

st.pyplot(fig)
plt.close(fig)

st.divider()

# Passengers by embarkation port
st.subheader("6. Passengers by Embarkation Port")

port_data = filtered_df["embarked"].value_counts()

fig, ax = plt.subplots()

ax.bar(port_data.index.astype(str), port_data.values)

ax.set_title("Passengers by Embarkation Port")
ax.set_xlabel("Embarkation Port")
ax.set_ylabel("Number of Passengers")

st.pyplot(fig)
plt.close(fig)

st.divider()

# Survival by age group
st.subheader("7. Survival by Age Group")

age_df = filtered_df.dropna(subset=["age", "survived"]).copy()

age_df["Age Group"] = pd.cut(
    age_df["age"],
    bins=[0, 12, 18, 35, 60, 100],
    labels=["Child", "Teenager", "Young Adult", "Adult", "Senior"]
)

age_group_data = age_df.groupby(
    ["Age Group", "survived"],
    observed=False
).size().unstack(fill_value=0)

fig, ax = plt.subplots()

age_group_data.rename(
    columns={0: "Did Not Survive", 1: "Survived"}
).plot(kind="bar", ax=ax)

ax.set_title("Survival by Age Group")
ax.set_xlabel("Age Group")
ax.set_ylabel("Number of Passengers")
ax.legend(title="Result")
ax.tick_params(axis="x", rotation=20)

st.pyplot(fig)
plt.close(fig)

st.divider()

# Passenger details
st.subheader("8. Passenger Details")

st.write("Passenger records based on the selected filters.")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.success("✅ Titanic Dashboard Loaded Successfully!")
