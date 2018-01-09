import hashlib
from collections import OrderedDict


class Transaction:
    def __init__(self, input_transaction_hash, recipient, quantity, signature=None):
        self.input_transaction_hash = input_transaction_hash
        self.recipient = recipient
        self.quantity = quantity
        self.signature = signature

    def get_hash(self):
        payload = str(OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity),
            ('signature', self.signature)
        ]))
        return hashlib.sha256(str.encode(payload)).hexdigest()

    def get_signature_payload(self):
        serialized = OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity)
        ])
        return str(serialized)

    def serialize(self):
        return OrderedDict([
            ('hash', self.get_hash()),
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity),
            ('signature', self.signature)
        ])

    @classmethod
    def deserialize(cls, serialized_transaction):
        return cls(
            serialized_transaction['input_transaction_hash'],
            serialized_transaction['recipient'],
            int(serialized_transaction['quantity']),
            serialized_transaction['signature'])
