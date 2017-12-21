from block import Block
from block_chain import BlockChain


class MessageProcessor:
    def __init__(self, message, network, block_chain, miner, public_key, difficulty):
        self.message = message
        self.network = network
        self.block_chain = block_chain
        self.miner = miner
        self.public_key = public_key
        self.difficulty = difficulty

    def process_messages(self):
        block_message = self.message.queues['block'].get()
        while block_message is not None:
            self._process_block_message(block_message)
            block_message = self.message.queues['block'].get()

        chain_request_message = self.message.queues['chain_request'].get()
        while chain_request_message is not None:
            self._process_chain_request_message(chain_request_message)
            chain_request_message = self.message.queues['chain_request'].get()

        chain_message = self.message.queues['chain'].get()
        while chain_message is not None:
            self._process_chain_message(chain_message)
            chain_message = self.message.queues['chain'].get()

        transaction_message = self.message.queues['transaction'].get()
        while transaction_message is not None:
            self._process_transaction_message(transaction_message)
            transaction_message = self.message.queues['transaction'].get()

    def _process_block_message(self, message):
        if message['height'] > (self.block_chain.tail.height + 1):
            print("I'm missing blocks")
            self.miner.stop()  # TODO: wait for this
            self.network.publish('chain_request', '')
            return
        if message['height'] <= self.block_chain.tail.height:
            print("Ignoring received block because our chain is longer")
            return
        # TODO: validate block
        print("Received a new block")
        self.miner.stop()
        new_block = Block(message['hashStr'], self.block_chain.tail, message['transactions'], message['nonce'],
                          message['height'])
        self.block_chain.append(new_block)
        self.miner.start(self.block_chain, self.public_key, self.difficulty)

    def _process_chain_request_message(self, message):
        print("Sending my chain")
        self.network.publish('chain', self.block_chain.serialize())

    def _process_chain_message(self, message):
        received_chain = BlockChain(message)
        if received_chain.length() <= self.block_chain.length():
            print("Ignoring received chain because our chain is longer")
            return
        # TODO: validate new chain
        print("Received a longer chain")
        self.miner.stop()
        self.block_chain.tail = received_chain.tail
        self.miner.start(self.block_chain, self.public_key, self.difficulty)

    def _process_transaction_message(self, message):
        raise Exception("not yet implemented")
