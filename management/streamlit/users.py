import streamlit as st
import requests
import pandas as pd
from datetime import datetime

USERS_URL = "http://127.0.0.1:8000/users/attendance/"


def fetch_users_attendance():
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    response = requests.get(USERS_URL, headers=headers)
    if response.status_code == 200:
        users = response.json()
        return users
    else:
        st.error("Failed to fetch students average grade.")
        return []


def users_page():
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.title("Users Attendance")

    data = fetch_users_attendance()

    df = pd.DataFrame(data)

    df['last_login'] = pd.to_datetime(df['last_login'])
    login_counts = df.groupby(df['last_login'].dt.date).size()
    st.line_chart(login_counts)
