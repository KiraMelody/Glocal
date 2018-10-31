
import uuid
import motor
import tornado.ioloop
import tornado.web
import tornado.gen
from tornado.options import define, options

import json
import bson

from redis import Redis

db = motor.MotorClient().glocal

define("port", default=8888, help="run on the given port", type=int)


redis = Redis()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_session(self):
        token = json.loads(self.request.body.decode("utf8"))["token"]
        return {'user': redis.get(token)}
    def get_current_user(self):
        if getattr(self, 'session', None) is None:
            self.session = self.get_current_session()
        return json.loads(self.request.body.decode("utf8"))["token"]
    def check_logout_state(self):
        print('user' not in self.session)
        print(self.session['user'])
        return 'user' not in self.session or self.session['user'] is None


class SignUpHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        if self.check_logout_state():
            data = json.loads(self.request.body.decode("utf8"))
            email, username = data["email"], data["username"]
            users = db.users.find({"email": email})
            if len(users) > 0:
                self.set_status(405)
                self.write(json.dumps({"msg": "Email or Username duplicates."}))
            else:
                yield db.users.insert({
                    "email": email, 
                    "username": username, 
                })
                self.set_status(200)
                self.write(json.dumps({"ok": "Sign up successfully."}))
        else:
            self.set_status(405)
            self.write(json.dumps({"error": "Please logout first."}))


application = tornado.web.Application([
    (r"/signup", SignUpHandler)], cookie_secret="ljhegrqkjfkajsbxkjcghwuer")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application.listen(options.port, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()


