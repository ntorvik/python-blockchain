from block import Block
from transaction import Transaction
from key_helper import KeyHelper
import settings


class BlockChain:
    def __init__(self, tail):
        if tail is None:
            self.tail = Block('00000e64d6cc039dd313efcab01114852ef7564af9a9f250ad24dfd200edd353', None, 0, 0)
            self.tail.add_transaction(Transaction(None, KeyHelper().get_public_key(), settings.REWARD, None))
        else:
            self.tail = tail

    def append(self, new_block):
        self.tail = new_block

    def serialize(self):
        serialized_chain = []
        block = self.tail
        while block is not None:
            serialized_chain.append(block.serialize())
            block = block.previous
        return serialized_chain

    @classmethod
    def deserialize(cls, serialized_block_chain):
        if serialized_block_chain is None:
            return cls(None)
        serialized_block = [block for block in serialized_block_chain if block['previous'] is None]
        tail = Block.deserialize(serialized_block[0], None)
        serialized_block = [block for block in serialized_block_chain if block['previous'] == tail.hash_str]
        while len(serialized_block) != 0:
            next_block = Block.deserialize(serialized_block[0], tail)
            tail = next_block
            serialized_block = [block for block in serialized_block_chain if block['previous'] == tail.hash_str]
        return cls(tail)
