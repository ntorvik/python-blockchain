import time
from miner import Miner
from block_chain import BlockChain
import file_helper
from queue import Queue
from network import Network
from message_processor import MessageProcessor
import settings
import key_helper

public_key = key_helper.get_public_key_str()
print("Loading blockchain")
serialized_block_chain = file_helper.load_blockchain()
block_chain = BlockChain.deserialize(serialized_block_chain)
message_queue = Queue()
transaction_queue = Queue()
network = Network(public_key, message_queue)
print("Starting miner")
miner = Miner(network, public_key, transaction_queue)
miner.start(block_chain, settings.DIFFICULTY)
print("Starting network listener")
message_processor = MessageProcessor(message_queue, network, block_chain, miner, public_key, settings.DIFFICULTY,
                                     transaction_queue)
message_processor.start()

network.publish('chain_request', block_chain.tail.height)


def main():
    print("Running")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting gracefully")
        miner.stop()
        message_processor.stop()


if __name__ == "__main__":
    main()
