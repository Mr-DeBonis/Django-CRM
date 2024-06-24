# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql mysql-connector-python

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv("dcrm.env", override=True)

dataBase = mysql.connector.connect(
    host="localhost",
    user=os.getenv("DB_USER"),
    passwd=os.getenv("DB_PASSWORD"),
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database
cursorObject.execute("CREATE DATABASE elderco")

print("All Done!")
