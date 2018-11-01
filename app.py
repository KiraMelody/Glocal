from flask import Flask, render_template, request, jsonify
import redis
import json
import re

app = Flask(__name__)
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


@app.route('/')
def mainpage():
	counter = int(r.get('counter'))
	r.set('counter', counter + 1)
	return render_template('index.html')

@app.route('/sign', methods = ['GET', 'POST'])
def sign():
	name = request.args.get("name")
	email = request.args.get("email")
	facebook = request.args.get("facebook")
	instagram = request.args.get("instagram")
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
	if match == None:
		return jsonify({'status': 'error', 'reason': 'Invalid Email!'})
	data = {'name': name, 'facebook': facebook, 'instagram': instagram}
	r.setnx(email, json.dumps(data))
	print(json.dumps(data))
	return jsonify({'status': 'success'})

if __name__ == '__main__':
	app.run()
