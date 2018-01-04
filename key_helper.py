from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
import settings


class KeyHelper:
    def __init__(self):
        with open(settings.PRIVATE_KEY_FILE, "r") as private_key_file:
            self.private_key = RSA.importKey(private_key_file.read())
        with open(settings.PUBLIC_KEY_FILE, "r") as public_key_file:
            self.public_key = RSA.importKey(public_key_file.read())

    def get_public_key(self):
        return self.public_key.exportKey().decode("utf-8")

    def sign(self, message):
        digest = SHA256.new()
        digest.update(message)
        signer = PKCS1_v1_5.new(self.private_key)
        return signer.sign(digest)

    @staticmethod
    def verify(message, signature, public_key_str):
        digest = SHA256.new()
        digest.update(message)
        public_key = RSA.importKey(public_key_str)
        verifier = PKCS1_v1_5.new(public_key)
        return verifier.verify(digest, signature)
