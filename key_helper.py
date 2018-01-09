from Cryptodome.Hash import SHA256
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.PublicKey import RSA
import settings
import binascii

with open(settings.PRIVATE_KEY_FILE, "r") as private_key_file:
    private_key = RSA.importKey(private_key_file.read())
with open(settings.PUBLIC_KEY_FILE, "r") as public_key_file:
    public_key = RSA.importKey(public_key_file.read())


def get_public_key():
    return public_key.exportKey().decode("utf-8")


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
