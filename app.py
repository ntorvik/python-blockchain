import time
import random
from miner import Miner
from block_chain import BlockChain
import file_helper
from queue import Queue
from network import Network
from message_processor import MessageProcessor

public_key = str(random.random())
difficulty = 5
serialized_block_chain = file_helper.load_blockchain()
block_chain = BlockChain.deserialize(serialized_block_chain)
message_queue = Queue()
network = Network(message_queue, public_key)

miner = Miner(network, public_key)
miner.start(block_chain, difficulty)

message_processor = MessageProcessor(message_queue, network, block_chain, miner, public_key, difficulty)
network.publish('chain_request', block_chain.tail.height)

try:
    message_processor.process_messages()
except KeyboardInterrupt:
    print("Exiting gracefully")
    miner.stop()
    network.disconnect()
