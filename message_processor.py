from block import Block
from block_chain import BlockChain
from validator import Validator
import threading


class MessageProcessor(threading.Thread):
    def __init__(self, message_queue, network, block_chain, miner, public_key, difficulty):
        threading.Thread.__init__(self)
        self.message_queue = message_queue
        self.network = network
        self.block_chain = block_chain
        self.miner = miner
        self.public_key = public_key
        self.difficulty = difficulty
        self.validator = Validator(block_chain)
        self.stopped = True
        self.message_processors = {
            'block': self._process_block_message,
            'chain': self._process_chain_message,
            'chain_request': self._process_chain_request_message,
            'transaction': self._process_transaction_message,
        }

    def run(self):
        self.stopped = False
        while not self.stopped:
            message = self.message_queue.get()
            if message['subject'] in self.message_processors:
                self.message_processors[message['subject']](message['payload'])

    def stop(self):
        self.stopped = True
        self.network.disconnect()
        self.message_queue.put({'subject': 'noop'})

    def _process_block_message(self, message):
        received_block = Block.deserialize(message, self.block_chain.tail)
        if received_block.height > (self.block_chain.tail.height + 1):
            print("I'm missing blocks")
            self.miner.stop()
            self.network.publish('chain_request', self.block_chain.tail.height)
            return
        if received_block.height <= self.block_chain.tail.height:
            print("Ignoring received block because our chain is longer")
            return
        valid = self.validator.validate_block(received_block)
        if not valid:
            print("Ignoring new block because it looks invalid")
            return
        print("Received a new block")
        self.miner.stop()
        self.block_chain.append(received_block)
        self.miner.start(self.block_chain, self.difficulty)

    def _process_chain_request_message(self, message):
        print("Sending my chain")
        self.network.publish('chain', self.block_chain.serialize())

    def _process_chain_message(self, message):
        received_chain = BlockChain.deserialize(message)
        if received_chain.tail.height <= self.block_chain.tail.height:
            print("Ignoring received chain because our chain is at least as long")
            return
        valid = self.validator.validate_chain(received_chain)
        if not valid:
            print("Ignoring new chain because it looks invalid")
            return
        print("Received a longer chain")
        self.miner.stop()
        self.block_chain.tail = received_chain.tail
        self.miner.start(self.block_chain, self.difficulty)

    def _process_transaction_message(self, message):
        raise Exception("not yet implemented")
