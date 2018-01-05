from block import Block
from block_chain import BlockChain


class MessageProcessor:
    def __init__(self, message_queue, network, block_chain, miner, public_key, difficulty):
        self.message_queue = message_queue
        self.network = network
        self.block_chain = block_chain
        self.miner = miner
        self.public_key = public_key
        self.difficulty = difficulty

        self.message_processors = {
            'block': self._process_block_message,
            'chain': self._process_chain_message,
            'chain_request': self._process_chain_request_message,
            'transaction': self._process_transaction_message,
        }

    def process_messages(self):
        message = self.message_queue.get()
        while True:
            self.message_processors[message['subject']](message['payload'])
            message = self.message_queue.get()

    def _process_block_message(self, message):
        if message['height'] > (self.block_chain.tail.height + 1):
            print("I'm missing blocks")
            self.miner.stop()  # TODO: wait for this
            self.network.publish('chain_request', self.block_chain.tail.height)
            return
        if message['height'] <= self.block_chain.tail.height:
            print("Ignoring received block because our chain is longer")
            return
        # TODO: validate block
        print("Received a new block")
        self.miner.stop()
        new_block = Block(message['hash_str'], self.block_chain.tail, message['transactions'], message['nonce'],
                          message['height'])
        self.block_chain.append(new_block)
        self.miner.start(self.block_chain, self.difficulty)

    def _process_chain_request_message(self, message):
        print("Sending my chain")
        self.network.publish('chain', self.block_chain.serialize())

    def _process_chain_message(self, message):
        received_chain = BlockChain.deserialize(message)
        if received_chain.tail.height <= self.block_chain.tail.height:
            print("Ignoring received chain because our chain is at least as long")
            return
        # TODO: validate new chain
        print("Received a longer chain")
        self.miner.stop()
        self.block_chain.tail = received_chain.tail
        self.miner.start(self.block_chain, self.difficulty)

    def _process_transaction_message(self, message):
        raise Exception("not yet implemented")
