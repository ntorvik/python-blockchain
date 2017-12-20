from block import Block


class BlockChain:
    def __init__(self, serialized_block_chain):
        if serialized_block_chain is None:
            self.head = Block('00000e64d6cc039dd313efcab01114852ef7564af9a9f250ad24dfd200edd353', None, [], 0, 0)
            self.tail = self.head
        else:
            self.head, self.tail = self.deserialize(serialized_block_chain)

    def append(self, new_block):
        self.tail.next = new_block
        self.tail = new_block

    def serialize(self):
        serialized_chain = []
        block = self.head
        while block is not None:
            serialized_chain.append(block.serialize())
            block = block.next
        return serialized_chain

    def deserialize(self, serialized_block_chain):
        serialized_block = [block for block in serialized_block_chain if block['previous'] is None][0]
        head = Block(serialized_block['hashStr'], None, serialized_block['transactions'], serialized_block['nonce'], serialized_block['height'])
        tail = head
        while serialized_block['next'] is not None:
            serialized_block = [block for block in serialized_block_chain if block['hashStr'] == serialized_block['next']][0]
            next = Block(serialized_block['hashStr'], tail, serialized_block['transactions'], serialized_block['nonce'], serialized_block['height'])
            tail.next = next
            tail = next
        return head, tail
