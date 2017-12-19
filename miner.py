import hashlib
import time
from block import Block


class Miner:
    def mine(self, previous_block, public_key, difficulty):
        curr_hash = ''
        nonce = previous_block.nonce
        while not (curr_hash.startswith('0' * difficulty)):
            payload = public_key + previous_block.hashStr + str(nonce)
            curr_hash = hashlib.sha256(str.encode(payload)).hexdigest()
            nonce += 1
        return Block(curr_hash, previous_block, [], nonce)
