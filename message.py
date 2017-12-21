from queue import Queue


class Message:
    def __init__(self):
        self.queues = {
            'block': Queue(),
            'chain_request': Queue(),
            'chain': Queue(),
            'transaction': Queue()
        }
