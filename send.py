import sys
from network import Network
import key_helper
from transaction import Transaction
import file_helper
from block_chain import BlockChain


def main():
    if len(sys.argv) != 3:
        print("Usage: python send.py 1 SOME_PUBLIC_KEY")
        return

    public_key = key_helper.get_public_key_str()

    serialized_block_chain = file_helper.load_blockchain()
    block_chain = BlockChain.deserialize(serialized_block_chain)

    input_transaction = _find_unspent_transaction(block_chain, public_key)
    if input_transaction is None:
        print("You can't afford that")
        return

    network = Network(public_key)
    new_transaction = Transaction(input_transaction.get_hash(), sys.argv[2], sys.argv[1])
    network.publish("transaction", new_transaction.serialize())


def _find_unspent_transaction(block_chain, public_key):
    curr_block = block_chain.tail
    while curr_block is not None:
        for curr_transaction in curr_block.transactions:
            if curr_transaction.recipient == public_key and not _is_transaction_spent(curr_transaction.get_hash(),
                                                                                      block_chain, curr_block.height):
                return curr_transaction
        curr_block = curr_block.previous
    return None


def _is_transaction_spent(transaction_hash, block_chain, min_height):
    current_block = block_chain.tail
    while current_block is not None and current_block.height > min_height:
        transaction = [t for t in current_block.transactions if t.input_transaction_hash == transaction_hash]
        if len(transaction) != 0:
            return True
        current_block = current_block.previous
    return False


if __name__ == "__main__":
    main()
