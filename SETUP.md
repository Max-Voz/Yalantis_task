##Install
____
**Be sure to use the Python version > 3.9.0.**
---
To install the application:

    # clone the repository
    $ git clone https://github.com/Max-Voz/Yalantis_task
    $ cd Yalantis_task
    
Create a virtualenv and activate it:

    $ python3 -m venv venv
    $ .venv/bin/activate

Or on Windows cmd:

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install all needed libraries, provided in requirements.txt:

    $ pip install -r requirements.txt

##Run
____
Navigate to the root folder of downloaded application and execute command from command prompt:

    $ flask run

Same for Windows cmd:

    > flask run

Perform an appropriate API calls to the http://127.0.0.1:5000 via [Postman](https://www.postman.com/) 
or [Insomnia](https://insomnia.rest/) or any other software which allows to perform API Calls. All appropriate 
endpoints and their usage are described in README.md

##Adding migrations
____
Initial migration of the database is included in the repository. After performing any change of database structure 
(app/models.py) it is needed to perform a migration (same for command prompt and Windows cmd):
    
    $ flask db migrate -m "Another migration."
    $ flask db upgrade

After this the application database (app.db) will be updated according to the performed changes.