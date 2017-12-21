import redis
import threading
import json


class Network:
    def __init__(self, message, public_key):
        self.connection = redis.Redis()
        self.public_key = public_key
        self.listener = self.Listener(message, public_key)
        self.listener.start()

    def publish(self, channel, data):
        print("Sending message to: " + channel)
        self.connection.publish(channel, json.dumps({'sender': self.public_key, 'payload': data}))

    def disconnect(self):
        self.listener.pubsub.unsubscribe()

    class Listener(threading.Thread):
        def __init__(self, message, public_key):
            threading.Thread.__init__(self)
            self.pubsub = redis.Redis().pubsub()
            self.message = message
            self.public_key = public_key
            self.pubsub.subscribe(message.queues.keys())

        def run(self):
            for message in self.pubsub.listen():
                channel = message['channel'].decode("utf-8")
                if message['type'] != 'message':
                    print("Ignoring extra message types")
                    continue
                data = json.loads(message['data'].decode("utf-8"))
                if channel not in self.message.queues.keys():
                    print("I don't recognize channel: " + channel)
                    continue
                if data['sender'] == self.public_key:
                    print('Ignoring message because I sent it.')
                    continue
                self.message.queues[channel].put(data['payload'])
