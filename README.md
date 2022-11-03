
# photo-management-application

photo-renovation-website is a Python project that allows you to manage, export, 
and retrieve information about photos that you can upload in several ways. 
This project uses, among others [Django](https://www.djangoproject.com/) and 
[Django REST framework](https://www.django-rest-framework.org/). 
Bootstrap was used to create the frontend.


## Setup project

* Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html) in the target folder (optional).
* Clone the repository:

![Alt text](Simple_application.png?raw=true)
```
  git clone https://github.com/AdrianGuzniczak/photo-management-application
```
* Install dependencies:

```
  pip3 install -r requirements.txt
```

* Create a development database:
```
  ./manage.py migrate
```

* Start the Django development server:
```
  ./manage.py runserver
```


Open your browser and go to http://127.0.0.1:8000