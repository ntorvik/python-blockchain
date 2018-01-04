from transaction import Transaction

class Block:
    def __init__(self, hashStr, previous, transactions, nonce, height):
        self.hashStr = hashStr
        self.previous = previous
        self.nonce = nonce
        self.height = height
        self.transactions = transactions

    def serialize(self):
        return {
            'hashStr': self.hashStr,
            'previous': self.previous.hashStr if self.previous else None,
            'nonce': self.nonce,
            'height': self.height,
            'transactions': [t.serialize() for t in self.transactions]
        }

    @classmethod
    def deserialize(cls, sb, previous):
        return cls(
            sb['hashStr'],
            previous,
            [Transaction.deserialize(t) for t in sb['transactions']],
            sb['nonce'],
            sb['height'])
