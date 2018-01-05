from transaction import Transaction
from merkletools import MerkleTools


class Block:
    def __init__(self, hash_str, previous, transactions, nonce, height):
        self.hash_str = hash_str
        self.previous = previous
        self.nonce = nonce
        self.height = height
        self.transactions = transactions

    def get_merkle_root(self):
        mt = MerkleTools()
        [mt.add_leaf(str(t.serialize()), True) for t in self.transactions]
        mt.make_tree()
        return mt.get_merkle_root()

    def serialize(self):
        return {
            'hash_str': self.hash_str,
            'previous': self.previous.hash_str if self.previous else None,
            'nonce': self.nonce,
            'height': self.height,
            'transactions': [t.serialize() for t in self.transactions]
        }

    @classmethod
    def deserialize(cls, sb, previous):
        return cls(
            sb['hash_str'],
            previous,
            [Transaction.deserialize(t) for t in sb['transactions']],
            sb['nonce'],
            sb['height'])
