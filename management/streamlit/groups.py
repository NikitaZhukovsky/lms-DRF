import streamlit as st
import requests

COURSES_URL = "http://127.0.0.1:8000/catalog/courses/{course_id}/"
GROUP_URL = "http://127.0.0.1:8000/study/groups/"
GROUP_AVERAGE_GRADE_URL = "http://127.0.0.1:8000/study/{group_id}/average-grade/"


def fetch_group_average_grade(group_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    url = GROUP_AVERAGE_GRADE_URL.format(group_id=group_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        group_average_grade = response.json().get("group_average_grade")
        return group_average_grade
    else:
        st.error("Failed to fetch group average grade.")
        return None


def fetch_groups():
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    response = requests.get(GROUP_URL, headers=headers)
    if response.status_code == 200:
        groups = response.json()
        return groups
    else:
        st.error("Failed to fetch groups.")
        return []


def fetch_course_name(course_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    url = COURSES_URL.format(course_id=course_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        course_name = response.json().get("title")
        return course_name
    else:
        st.error(f"Failed to fetch course name for course ID {course_id}.")
        return None


def groups_page(groups):
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.title("Groups Average Grade")
    if len(groups) > 0:
        group_data = []
        for group in groups:
            course_name = fetch_course_name(group["course"])
            if course_name is None:
                course_name = "Unknown"
            group_average_grade = fetch_group_average_grade(group["id"])
            if group_average_grade is None:
                group_average_grade = 0
            group_info = {
                "id": group["id"],
                "Name": group["name"],
                "Course": course_name,
                "Average": group_average_grade
            }
            group_data.append(group_info)

        st.table(group_data)
        st.title("Groups Average Grade")
        st.bar_chart(group_data, x="Name", y="Average", color="Course", width=800)
    else:
        st.write("No groups available.")
