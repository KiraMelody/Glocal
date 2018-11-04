# -*- coding: utf-8 -*-

# ------------------------------------
# File  : app.py
# Date  : 2018/10/27 2:16 PM
# Author: KiraMelody
# -----------------------------------

from flask import Flask, render_template, request, jsonify, g
from db import SQLALCHEMY_DATABASE_LOC
import sqlite3
import json
import re

app = Flask(__name__)

@app.before_request
def before_request():
	g.conn = sqlite3.connect(SQLALCHEMY_DATABASE_LOC)
	g.cursor = g.conn.cursor()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'cursor'):
		g.cursor.close()
	if hasattr(g, 'conn'):
		g.conn.close()

@app.route('/')
def mainpage():
	counter = int(g.cursor.execute("SELECT MAX(id) FROM counter").fetchall()[0][0]) + 1
	g.cursor.execute("INSERT INTO counter VALUES ('%d')" % counter)
	g.conn.commit()
	return render_template('index.html')

@app.route('/sign', methods = ['GET', 'POST'])
def sign():
	print g.cursor.execute("SELECT MAX(id) FROM user").fetchall()
	total_user_num = int(g.cursor.execute("SELECT MAX(id) FROM user").fetchall()[0][0]) + 1
	id = '0' * (5 - len(str(total_user_num))) + str(total_user_num)
	email = request.args.get("email")
	country = request.args.get("country")
	platform = request.args.get("platform")
	account = request.args.get("account")
	followers = request.args.get("followers")
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
	if match == None:
		return jsonify({'status': 'error', 'reason': 'Invalid Email!'})
	try:
		followers = int(followers)
	except:
		return jsonify({'status': 'error', 'reason': 'Invalid Followers Format!'})
	user_exist = g.cursor.execute("SELECT * FROM user WHERE email = '%s'"
	                              % (email)).fetchall()
	if user_exist:
		return jsonify({'status': 'error', 'reason': 'Duplicate Email!'})

	g.cursor.execute("INSERT INTO user VALUES ('%s', '%s', '%s', '%s','%s', '%d')"
	                 % (id, email, country, platform, account, followers))
	g.conn.commit()
	return jsonify({'status': 'success'})

if __name__ == '__main__':
	app.run()
