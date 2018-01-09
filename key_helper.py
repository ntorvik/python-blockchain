from Cryptodome.PublicKey import RSA
import settings

with open(settings.PRIVATE_KEY_FILE, "r") as private_key_file:
    private_key = RSA.importKey(private_key_file.read())
with open(settings.PUBLIC_KEY_FILE, "r") as public_key_file:
    public_key = RSA.importKey(public_key_file.read())


def get_public_key_str():
    return public_key.exportKey().decode("utf-8")
