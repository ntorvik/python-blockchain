import time
import random
from miner import Miner
from block_chain import BlockChain
import file_helper
from message import Message
from network import Network
from message_processor import MessageProcessor

public_key = str(random.random())
difficulty = 6
serialized_block_chain = file_helper.load_blockchain()
block_chain = BlockChain(serialized_block_chain)
message = Message()
network = Network(message, public_key)

miner = Miner(network)
miner.start(block_chain, public_key, difficulty)

message_processor = MessageProcessor(message, network, block_chain, miner, public_key, difficulty)

try:
    while True:
        message_processor.process_messages()
        time.sleep(5)
except KeyboardInterrupt:
    print("Exiting gracefully")
    miner.stop()
    network.disconnect()
