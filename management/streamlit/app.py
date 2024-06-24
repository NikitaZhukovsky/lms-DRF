import streamlit as st
import requests
from groups import fetch_groups, groups_page
from students import fetch_students_average_grade, students_page, fetch_attendance_percentage

LOGIN_URL = "http://127.0.0.1:8000/users/auth/jwt/create/"


def main():
    if "access_token" not in st.session_state:
        logged_in = False
    else:
        logged_in = True

    with st.sidebar:
        st.title("User Login")

        if not logged_in:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.sidebar.button("Login"):
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

                        st.session_state["access_token"] = access_token
                        st.session_state["refresh_token"] = refresh_token
                        logged_in = True
                    else:
                        st.error("Failed to retrieve access token.")
                else:
                    st.error("Login failed. Please try again.")
        else:
            st.info("Welcome!")

        selection = st.sidebar.radio("Select an option", ("Groups", "Students"))

    if logged_in:
        if selection == "Groups":
            groups = fetch_groups()
            groups_page(groups)
        elif selection == "Students":
            students = fetch_students_average_grade()
            attendance_percentage = fetch_attendance_percentage()
            students_page(students,  attendance_percentage)


if __name__ == "__main__":
    main()