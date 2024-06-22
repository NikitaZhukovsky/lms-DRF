import streamlit as st
import requests
from groups import fetch_groups, groups_page

LOGIN_URL = "http://127.0.0.1:8000/users/auth/jwt/create/"


def main():
    st.set_page_config(page_title="User Login")
    with st.sidebar:
        st.title("User Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            data = {
                "email": email,
                "password": password
            }
            response = requests.post(LOGIN_URL, json=data)

            if response.status_code == 200:
                access_token = response.json().get("access")
                refresh_token = response.json().get("refresh")

                if access_token:
                    st.success("Login successful!")
                    st.info("Welcome!")

                    if "access_token" not in st.session_state:
                        st.session_state["access_token"] = access_token
                    if "refresh_token" not in st.session_state:
                        st.session_state["refresh_token"] = refresh_token
                else:
                    st.error("Failed to retrieve access token.")
            else:
                st.error("Login failed. Please try again.")

    groups = fetch_groups() if st.session_state.get("access_token") else []
    groups_page(groups)


if __name__ == "__main__":
    main()
