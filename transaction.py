class Transaction:
    def __init__(self, input_transaction, recipient, quantity, signature):
        self.input_transaction = input_transaction
        self.recipient = recipient
        self.quantity = quantity
        self.signature = signature

    def serialize(self):
        return {
            'input_transaction': self.input_transaction,
            'recipient': self.recipient,
            'quantity': self.quantity,
            'signature': self.signature
        }

    @classmethod
    def deserialize(cls, sb):
        return cls(sb['input_transaction'], sb['recipient'], sb['quantity'], sb['signature'])
