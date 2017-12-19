import hashlib
import time
from block import Block
from miner import Miner
from block_chain import BlockChain

block_chain = BlockChain()

miner = Miner()

while True:
    new_block = miner.mine(block_chain.tail, 'my public key', 5)
    block_chain.append(new_block)
    print("Mined block: " + new_block.hashStr)









