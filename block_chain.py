from block import Block


class BlockChain:
    def __init__(self, serialized_block_chain):
        if serialized_block_chain is None:
            self.head = Block('00000e64d6cc039dd313efcab01114852ef7564af9a9f250ad24dfd200edd353', None, [], 0)
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
        serialized_head = [block for block in serialized_block_chain if block['previous'] is None][0]
        head = Block(serialized_head['hashStr'], None, serialized_head['transactions'], serialized_head['nonce'])
        tail = head
        serialized_tail = serialized_head
        while serialized_tail['next'] is not None:
            serialized_tail = [block for block in serialized_block_chain if block['hashStr'] == serialized_tail['next']][0]
            next = Block(serialized_tail['hashStr'], tail, serialized_tail['transactions'], serialized_tail['nonce'])
            tail.next = next
            tail = next
        return head, tail
