from block import Block


class BlockChain:
    def __init__(self):
        self.head = Block('00000e64d6cc039dd313efcab01114852ef7564af9a9f250ad24dfd200edd353', None, [], 0)
        self.tail = self.head

    def append(self, new_block):
        self.tail.next = new_block
        self.tail = new_block
