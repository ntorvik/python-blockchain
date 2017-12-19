class Block:
    def __init__(self, hashStr, previous, transactions, nonce):
        self.hashStr = hashStr
        self.next = None
        self.previous = previous
        self.nonce = nonce
        self.transactions = transactions


