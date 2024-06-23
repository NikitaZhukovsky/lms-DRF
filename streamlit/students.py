import streamlit as st
import requests

STUDENTS_URL = "http://127.0.0.1:8000/users/students/{id}/"
AVERAGE_GRADE_URL = "http://127.0.0.1:8000/study/students/average-grade/"
ATTENDANCE_PERCENTAGE_URL = "http://127.0.0.1:8000/study/students/attendance_percentage/"

def fetch_students_average_grade():
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    response = requests.get(AVERAGE_GRADE_URL, headers=headers)
    if response.status_code == 200:
        students = response.json()
        return students
    else:
        st.error("Failed to fetch students average grade.")
        return []

def fetch_attendance_percentage():
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    response = requests.get(ATTENDANCE_PERCENTAGE_URL, headers=headers)
    if response.status_code == 200:
        attendance_percentage = response.json()["attendance_percentage"]
        return attendance_percentage
    else:
        st.error("Failed to fetch attendance percentage.")
        return []

def fetch_student_info(student_id):
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token')}"
    }
    url = STUDENTS_URL.format(id=student_id)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        student_info = response.json()
        return student_info
    else:
        st.error(f"Failed to fetch student info for student ID {student_id}.")
        return None

def students_page(students, attendance_percentage):
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.title("Students Average Grade and Attendance")

    if len(students) > 0:
        student_data = []
        for student in students:
            student_id = student["student_id"]
            student_info = fetch_student_info(student_id)
            if student_info is not None:
                student_name = f"{student_info['first_name']} {student_info['last_name']}"
                student_average_grade = student["average_grade"]

                attendance = next((item for item in attendance_percentage if item["student_id"] == student_id), None)
                student_attendance_percentage = attendance["attendance_percentage"] if attendance else "-"

                student_data.append({
                    "ID": student_id,
                    "Name": student_name,
                    "Average Grade": student_average_grade,
                    "Attendance Percentage": student_attendance_percentage
                })

        st.table(student_data)

        student_names = [data["Name"] for data in student_data]
        average_grades = [data["Average Grade"] for data in student_data]
        attendance_percentages = [data["Attendance Percentage"] for data in student_data]

        st.title("Students Average Grade")
        st.bar_chart(dict(zip(student_names, average_grades)))

        st.title("Students Attendance Percentage")
        st.bar_chart(dict(zip(student_names, attendance_percentages)))
    else:
        st.write("No students available.")


students = fetch_students_average_grade()
attendance_percentage = fetch_attendance_percentage()
students_page(students, attendance_percentage)