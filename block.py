from transaction import Transaction
from merkletools import MerkleTools


class Block:
    def __init__(self, hash_str, previous, nonce, height, merkle_root=None, transactions=None):
        self.hash_str = hash_str
        self.previous = previous
        self.nonce = nonce
        self.height = height
        self.transactions = [] if transactions is None else transactions
        self.merkle_root = merkle_root
        self._mt = MerkleTools()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self._mt.add_leaf(str(transaction.serialize()), True)
        self._mt.make_tree()
        self.merkle_root = self._mt.get_merkle_root()

    def serialize(self):
        return {
            'hash': self.hash_str,
            'previous': self.previous.hash_str if self.previous else None,
            'nonce': self.nonce,
            'height': self.height,
            'merkle_root': self.merkle_root,
            'transactions': [t.serialize() for t in self.transactions]
        }

    @classmethod
    def deserialize(cls, serialized_block, previous):
        return cls(
            serialized_block['hash'],
            previous,
            serialized_block['nonce'],
            serialized_block['height'],
            serialized_block['merkle_root'],
            [Transaction.deserialize(t) for t in serialized_block['transactions']])
