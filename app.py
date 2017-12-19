from miner import Miner
from block_chain import BlockChain
import file_helper

serialized_block_chain = file_helper.load_blockchain()
block_chain = BlockChain(serialized_block_chain)
miner = Miner()

# while True:
#     new_block = miner.mine(block_chain.tail, 'my public key', 5)
#     block_chain.append(new_block)
#     file_helper.save_blockchain(block_chain.serialize())
#     print("Mined block: " + new_block.hashStr)


file_helper.save_blockchain(block_chain.serialize())






