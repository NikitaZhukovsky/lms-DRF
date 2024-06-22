import streamlit as st
import requests

COURSES_URL = "http://127.0.0.1:8000/catalog/courses/{course_id}"
GROUP_URL = "http://127.0.0.1:8000/study/groups/"
GROUP_AVERAGE_GRADE_URL = "http://127.0.0.1:8000/study/groups/{group_id}/average-grade/"
