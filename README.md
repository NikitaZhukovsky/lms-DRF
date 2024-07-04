# Learning management system using Django REST Framework
Feature-rich learning management system. You may want to build a learning management system for a school organization or just for the sake of learning the tech stack, either way, this project would be a good kickstart for you.
## Current features:

- Registration and authentication (JWT) of users with email confirmation.
- Editing a user's profile.
- Assigning “Teacher” roles to teachers.
- Connecting users to the course, viewing users on the course, removing a user from the course.
- Getting a list of all teachers.
- Getting information about the teacher by id.
- Getting a list of all students.
- Getting information about a student by id.
- Create, receive, edit, and delete courses.
- Creating, receiving, editing, and deleting course modules.
- Create, receive, edit, and delete lessons.
- Storing all files on Yandex Cloud, as well as the ability to receive all files, a separate file by id and delete the file.
- Rating students for a lesson.
- Calculating the average score of students and groups.
- When you connect to the course, you will receive an email message.
- In case of any change in the course or class, sending a message to students connected to the course by email.
- Generating reports on academic performance and attendance.
- An application on Streamlit to get statistics on the average score and attendance of classes.
- Swagger  
- Prospector
- Pytest  
- CI  

# Database Models:
![db-scheme](https://github.com/NikitaZhukovsky/lms-DRF/blob/master/assets/lms.png)

# Streamlit:
Groups average grade:  
<p align="center">
  <img src="https://github.com/NikitaZhukovsky/lms-DRF/blob/master/assets/groups_average.png" alt="Groups average grade" width="500"/>
</p>  
Students average grade:
<p align="center">
  <img src="https://github.com/NikitaZhukovsky/lms-DRF/blob/master/assets/students_average.png" alt="Students average grade" width="500"/>
</p>  


  # Requirements:
- Python3.8+
- PostgreSQL
- RabbitMQ
- Postman  
- Yandex Cloud account
- Docker

# Installation
- Clone the repo with

```bash
https://github.com/NikitaZhukovsky/lms-DRF.git
```
```bash
pip install -r requirements.txt
```

- Create `.env` file inside the root directory and include the following variables
  
SECRET_KEY=YOUR_SECRET_KEY  
DATABASE_NAME=YOUR_DATABASE_NAME  
DATABASE_USER=YOUR_DATABASE_USER  
DATABASE_PASSWORD=YOUR_DATABASE_PASSWORD  
DATABASE_HOST=localhost  
DATABASE_PORT=YOUR_POSTGRES_PORT default is 5432  
EMAIL_HOST_USER=YOUR_EMAIL  
EMAIL_HOST_PASSWORD=YOUR_EMAIL-PASSWORD  
CELERY_HOST=YOUR_HOST  
CELERY_PORT=YOUR_PORT  
BUCKET_NAME=YOUR_BUCKET_NAME  
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID  
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY  
ENDPOINT_URL=https://storage.yandexcloud.net  
REGION_NAME=YOUT_REGION_NAME    
DJANGO_SUPERUSER_PASSWORD=YOUR_DJANGO_SUPERUSER_PASSWORD  
DJANGO_SUPERUSER_EMAIL=YOUR_DJANGO_SUPERUSER_EMAIL  

# Starting:
```bash
cd management
```

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

```bash
python manage.py runserver
```
# Start Сelery:
```bash
cd management
```
```bash
celery --app management worker --pool=solo -l info
```
Once a month, students are sent a report on their average grade.  
# Starting Streamlit:
```bash
cd management
```

```bash
cd streamlit
```

```bash
streamlit run app.py
```

Last but not least, go to this address http://127.0.0.1:8000 and streamlit: http://localhost:8501  
To get the API documentation, you can add it to the url **/doc** and swagger will open.
# Postman:
You can import the `LMS.postman_collection collection.json` from management to postman.

# Email notifications:
- When adding a student to a course.
- When a student is removed from the course.
- When adding a student to a group.  
- When adding a student to a group.
- When removing a student from a group.  
- When adding new material for classes.
- When deleting lesson material.  

# Pytest:
- Test for creating and deleting a course.  
- Test for creating and deleting a course module.
- Test for creating and deleting a lesson.
- Test for creating a group.
- Auth test.

To run the tests, you need to:  
```bash
cd management
```

```bash
pytest
```
# Prospector:
To start the prospector, you need to enter the command:
```bash
prospector
```

# Alternatively, you can create a container from a Docker image:
```bash
cd management
```
```bash
docker-compose up --build
```
Previously, in the `.env` file, you need to change the following parameters:  

DATABASE_HOST=db   
CELERY_HOST=rabbitmq    

And in `settings.py` change the line:  

CELERY_BROKER_URL='amqp://guest:guest@rabbitmq:5672/' 


