import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
import db
import json
import datetime

class FlagReceiverSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        flag = db.models.Flag.select().where(db.models.Flag.flag == message).first()
        game = db.models.Game.select().first()
        if flag and game.running:
            submit = db.models.Submit.select().where(db.models.Submit.flag == flag).first()
            if not submit:
                db.models.Submit.create(flag=flag)
                game.score -= 5
                game.save()

    def open(self):
        self.write_message(u'Send us "your" flags (one per line):')

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", FlagReceiverSocket),
    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(1337)
    tornado.ioloop.IOLoop.instance().start()