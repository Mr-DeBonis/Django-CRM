<!-- TOC -->
* [Django CRM](#django-crm)
* [Features](#features)
* [Setup & Other settings](#setup--other-settings)
  * [Installation](#installation)
  * [Database migration](#database-migration)
<!-- TOC -->

# Django CRM

A CRM based on Django. This is my follow up from the tutorial shown [here](https://www.youtube.com/watch?v=t10QcFx7d5k) by codemy.com

# Features

Very bare bones CRM. It allows you to: add, edit and remove information from customers:
* Email
* Phone
* Address
* City
* State
* Zipcode
* Creation date

# Setup & Other settings
## Installation

1. Use Python 3.11 (Create a virtual environment)
2. Install requirements
    ```
    pip install -r requirements.txt
    ```
3. Install [mysql](https://dev.mysql.com/downloads/installer/)
4. **On windows:** Run it by executing `services.msc`and start the service
5. Create an environment file:
   ```
    DB_USER=****
    DB_PASSWORD=****
    DB_HOST=****
    DB_PORT=****
    
    SUPERUSER=****
    SUPERUSER_EMAI=****
    SUPERUSER_PASSWORD=****
    ```

6. You're all set!

##  Database migration

1. After creating a model, run:
`python manage.py makemigrations`
2. To load to DB: 
`python manage.py migrate`