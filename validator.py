import hashlib
from key_helper import KeyHelper
import settings


class Validator:
    def __init__(self, block_chain):
        self.block_chain = block_chain

    def validate_chain(self, new_chain):
        current_block = new_chain.tail
        while current_block.previous is not None:
            block_valid = self.validate_block(current_block, current_block.previous)
            if not block_valid:
                return False
            current_block = current_block.previous
        return True

    def validate_block(self, new_block, tail=None):
        tail = tail if tail is not None else self.block_chain.tail
        reward_transactions = sum([1 for t in new_block.transactions if t.input_transaction_hash is None])
        if reward_transactions != 1:
            return False
        transactions_valid = all(self.validate_transaction(t) for t in new_block.transactions)
        if not transactions_valid:
            return False
        payload = new_block.merkle_root + tail.hash_str + str(new_block.nonce)
        computed_hash_str = hashlib.sha256(str.encode(payload)).hexdigest()
        if new_block.hash_str != computed_hash_str:
            return False
        if new_block.height != tail.height + 1:
            return False
        if not new_block.hash_str.startswith('0' * settings.DIFFICULTY):
            return False
        return True

    def validate_transaction(self, transaction):
        if transaction.input_transaction_hash is None:
            if transaction.quantity != settings.REWARD:
                return False
            return True
        input_transaction = self._find_transaction(transaction.input_transaction_hash)
        if input_transaction is None:
            return False
        # TODO: validate transaction is not spent
        signature_verified = KeyHelper.verify(transaction, input_transaction.recipient)
        if not signature_verified:
            return False
        if not input_transaction.quantity == transaction.quantity:
            return False
        return True

    def _find_transaction(self, transaction_hash):
        current_block = self.block_chain.tail
        while current_block is not None:
            transaction = [t for t in current_block.transactions if t.get_hash() == transaction_hash]
            if len(transaction) != 0:
                return transaction[0]
            current_block = current_block.previous
        return None
