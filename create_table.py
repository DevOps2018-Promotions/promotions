import pymysql
from models import db

conn = pymysql.connect(host='localhost', user='root', password='9527')
conn.cursor().execute('CREATE DATABASE IF NOT EXISTS Promotion')