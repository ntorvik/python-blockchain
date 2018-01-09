from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
import settings
import binascii


class KeyHelper:
    def __init__(self):
        with open(settings.PRIVATE_KEY_FILE, "r") as private_key_file:
            self.private_key = RSA.importKey(private_key_file.read())
        with open(settings.PUBLIC_KEY_FILE, "r") as public_key_file:
            self.public_key = RSA.importKey(public_key_file.read())

    def get_public_key(self):
        return self.public_key.exportKey().decode("utf-8")

    @staticmethod
    def verify(transaction, public_key_str):
        payload = transaction.get_signature_payload()
        digest = SHA256.new(str.encode(payload))
        public_key = RSA.importKey(public_key_str)
        verifier = PKCS1_v1_5.new(public_key)
        signature = binascii.unhexlify(transaction.signature)
        try:
            verifier.verify(digest, signature)
            return True
        except Exception:
            return False
