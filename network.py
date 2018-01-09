import redis
import threading
import json


class Network:
    def __init__(self, public_key, message_queue=None):
        self.connection = redis.Redis()
        self.public_key = public_key
        if message_queue is not None:
            self.listener = self.Listener(message_queue, public_key)
            self.listener.start()

    def publish(self, subject, data):
        self.connection.publish('blockchain', json.dumps({'sender': self.public_key, 'subject': subject, 'payload': data}))

    def disconnect(self):
        self.listener.pubsub.unsubscribe()

    class Listener(threading.Thread):
        def __init__(self, message_queue, public_key):
            threading.Thread.__init__(self)
            self.pubsub = redis.Redis().pubsub()
            self.message_queue = message_queue
            self.public_key = public_key
            self.pubsub.subscribe(['blockchain'])

        def run(self):
            for message in self.pubsub.listen():
                if message['type'] != 'message':
                    continue
                data = json.loads(message['data'].decode("utf-8"))
                if data['sender'] == self.public_key:
                    continue
                self.message_queue.put(data)
