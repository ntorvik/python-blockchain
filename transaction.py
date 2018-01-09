import hashlib
from collections import OrderedDict
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
import binascii
import key_helper


class Transaction:
    def __init__(self, input_transaction_hash, recipient, quantity, signature=None):
        self.input_transaction_hash = input_transaction_hash
        self.recipient = recipient
        self.quantity = quantity
        self.signature = signature if signature is not None else self._sign()

    def _sign(self):
        payload = OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity)
        ])
        digest = SHA256.new(str.encode(str(payload)))
        signer = PKCS1_v1_5.new(key_helper.private_key)
        signature = signer.sign(digest)
        return binascii.hexlify(signature).decode("utf-8")

    def verify_signature(self, public_key_str):
        payload = OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity)
        ])
        digest = SHA256.new(str.encode(str(payload)))
        public_key = RSA.importKey(public_key_str)
        verifier = PKCS1_v1_5.new(public_key)
        signature = binascii.unhexlify(self.signature)
        try:
            verifier.verify(digest, signature)
            return True
        except Exception:
            return False

    def get_hash(self):
        payload = str(OrderedDict([
            ('input_transaction_hash', self.input_transaction_hash),
            ('recipient', self.recipient),
            ('quantity', self.quantity),
            ('signature', self.signature)
        ]))
        return hashlib.sha256(str.encode(payload)).hexdigest()

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
