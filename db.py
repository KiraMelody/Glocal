# -*- coding: utf-8 -*-

# ------------------------------------
# File  : db.py
# Date  : 2018/11/1 11:57 PM
# Author: KiraMelody
# ------------------------------------

import  sqlite3
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_LOC = os.path.join(basedir, 'glocal.db')

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

def main():
	# connect to database
	conn = sqlite3.connect(SQLALCHEMY_DATABASE_LOC)
	cursor = conn.cursor()
	try:
		cursor.execute("""DROP TABLE user""")
		cursor.execute("""DROP TABLE counter""")
	except:
		print("do not exist")
	cursor.execute("""CREATE TABLE user(
	id CHAR(5) NOT NULL,
	email CHAR(20) NOT NULL,
	country CHAR(20),
	platform CHAR(10) ,
	account  CHAR(40) ,
	followers SMALLINT,
	PRIMARY KEY(id)
	);
	""")
	cursor.execute("INSERT INTO user VALUES ('00000', 'none', NULL , NULL , NULL , NULL );")
	cursor.execute("""CREATE TABLE counter(
	id SMALLINT NOT NULL,
	PRIMARY KEY(id)
	);
	""")

	cursor.execute("INSERT INTO counter VALUES (1);")
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	main()
