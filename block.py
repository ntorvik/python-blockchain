class Block:
    def __init__(self, hashStr, previous, transactions, nonce):
        self.hashStr = hashStr
        self.next = None
        self.previous = previous
        self.nonce = nonce
        self.transactions = transactions

    def serialize(self):
        return {
            'hashStr': self.hashStr,
            'next': self.next.hashStr if self.next else None,
            'previous': self.previous.hashStr if self.previous else None,
            'nonce': self.nonce,
            'transactions': self.transactions
        }


