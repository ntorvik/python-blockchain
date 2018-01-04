import random
from miner import Miner
from block_chain import BlockChain
import file_helper
from queue import Queue
from network import Network
from message_processor import MessageProcessor
import settings

public_key = str(random.random())
serialized_block_chain = file_helper.load_blockchain()
block_chain = BlockChain.deserialize(serialized_block_chain)
message_queue = Queue()
network = Network(message_queue, public_key)

miner = Miner(network, public_key)
miner.start(block_chain, settings.DIFFICULTY)

message_processor = MessageProcessor(message_queue, network, block_chain, miner, public_key, settings.DIFFICULTY)
network.publish('chain_request', block_chain.tail.height)

try:
    message_processor.process_messages()
except KeyboardInterrupt:
    print("Exiting gracefully")
    miner.stop()
    network.disconnect()
