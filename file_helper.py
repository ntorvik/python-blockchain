import json


blockchain_file = 'blockchain.json'


def save_blockchain(serialized_block_chain):
    with open(blockchain_file, 'w') as outfile:
        json.dump(serialized_block_chain, outfile, indent=4)


def load_blockchain():
    try:
        with open(blockchain_file, 'r') as infile:
            serialized_block_chain = json.load(infile)
    except FileNotFoundError:
        return None
    return serialized_block_chain
