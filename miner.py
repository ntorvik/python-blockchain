import hashlib
import threading
import file_helper
from block import Block
from transaction import Transaction
import settings


class Miner:
    def __init__(self, network, public_key, transaction_queue):
        self.network = network
        self.public_key = public_key
        self.transaction_queue = transaction_queue
        self.thread = None

    def start(self, block_chain, difficulty):
        self.thread = self.MinerThread(block_chain, self.public_key, difficulty, self.network, self.transaction_queue)
        self.thread.start()

    def stop(self):
        self.thread.stop()
        self.thread.join()

    class MinerThread(threading.Thread):
        def __init__(self, block_chain, public_key, difficulty, network, transaction_queue):
            threading.Thread.__init__(self)
            self.block_chain = block_chain
            self.public_key = public_key
            self.difficulty = difficulty
            self.network = network
            self.transaction_queue = transaction_queue
            self.stopped = True

        def run(self):
            self.stopped = False
            while not self.stopped:
                self.mine()

        def stop(self):
            self.stopped = True

        def mine(self):
            new_block = Block('', self.block_chain.tail, self.block_chain.tail.nonce, self.block_chain.tail.height + 1)
            new_block.add_transaction(Transaction(None, self.public_key, settings.REWARD))
            while not self.transaction_queue.empty():
                new_block.add_transaction(self.transaction_queue.get())
            while not (new_block.hash_str.startswith('0' * self.difficulty)):
                if self.stopped:
                    return
                new_block.nonce += 1
                payload = new_block.merkle_root + self.block_chain.tail.hash_str + str(new_block.nonce)
                new_block.hash_str = hashlib.sha256(str.encode(payload)).hexdigest()
            print("Mined block: " + new_block.hash_str)

            self.block_chain.append(new_block)
            file_helper.save_blockchain(self.block_chain.serialize())
            self.network.publish('block', new_block.serialize())
