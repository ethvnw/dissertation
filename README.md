# Digitising the Extenuating Circumstances Process
This respository supplements the dissertation that was submitted as a part of the requirements for the degree of Master of Computer Science.

## Dissertation Abstract
Extenuating circumstances are unforeseen events that negatively affect a student’s ability to complete an assessment. The current process to submit an extenuating circumstance application involves a cumbersome hybrid of paper-based and online forms. The objectiv eof this project is to unify the process into a single, centralised system that may be accessed by students and staff of the university. There are many benefits to this unification, including a more secure and accessible approach to managing extenuating circumstances.

This dissertation details an extensive literature review that explores the security and accessibility methodologies that may be incorporated into an online system. Django was chosen as the web framework to realise the requirements of the project, due to its robust security features and scalability. The design adhered to accessibility guidelines and prioritised the security of user data. An evaluation of the system was conducted which concluded the system was successful in meeting its core objectives and identified areas for future work.

## Repository Information
This is a web application built using Django and Tailwind CSS. To initalise the system, run the following commands in a terminal:

1. `git clone https://github.com/ethvnw/dissertation.git`
2. `pip install -r requirements.txt`
3. If the server is running with `DEBUG=FALSE`:
    * `python manage.py collectstatic`
    * `python manage.py runserver --insecure`
  
4. Else:
    *  `python manage.py runserver`
5. In a separate terminal: `python manage.py tailwind start`
6. Access the server at `http://localhost:8000`
