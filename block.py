class Block:
    def __init__(self, hashStr, previous, transactions, nonce, height):
        self.hashStr = hashStr
        self.next = None
        self.previous = previous
        self.nonce = nonce
        self.height = height
        self.transactions = transactions

    def serialize(self):
        return {
            'hashStr': self.hashStr,
            'next': self.next.hashStr if self.next else None,
            'previous': self.previous.hashStr if self.previous else None,
            'nonce': self.nonce,
            'height': self.height,
            'transactions': self.transactions
        }


