import hashlib
from collections import OrderedDict


class Transaction:
    def __init__(self, input_transaction_hash, recipient, quantity, signature):
        self.input_transaction_hash = input_transaction_hash
        self.recipient = recipient
        self.quantity = quantity
        self.signature = signature

    def get_hash(self):
        payload = str(self.serialize())
        return hashlib.sha256(str.encode(payload)).hexdigest()

    def get_signature_payload(self):
        serialized = self.serialize()
        serialized.pop('signature')
        return str(serialized)

    def serialize(self):
        return OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity),
            ('signature', self.signature)
        ])

    @classmethod
    def deserialize(cls, sb):
        return cls(sb['input_transaction_hash'], sb['recipient'], sb['quantity'], sb['signature'])
