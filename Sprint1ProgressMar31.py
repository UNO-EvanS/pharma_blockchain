"""
A blockchain, which is a decentralized digital ledger where transactions are recorded.
The data is immutable and is distributed across multiple devices.
I have not yet decided how to make this unique.
"""

import hashlib

class MyCoinBlock: # Creates a block with its own unique hash using the transaction data and previous hash
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash # ensures blocks remain linked together
        self.transaction_list = transaction_list

        self.block_data = f"{' - '.join(transaction_list)} - {previous_block_hash}" # conjoins the transactions and hashes into a string
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest() # generates a hash using Secure Hash Algorithm 256-bit

class BlockChain:
    def __init__(self):
        self.chain = [] # holds all the blocks
        self.generate_genesis_block()

    def generate_genesis_block(self): # first block
        self.chain.append(MyCoinBlock("0", ['Genesis Block']))

    def create_transaction_block(self, transaction_list): # adds new block to the chain
        previous_block_hash = self.last_block.block_hash
        self.chain.append(MyCoinBlock(previous_block_hash, transaction_list))

    def display_chain(self): # displays all the data within each block, including their hash values
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}\n")

    @property
    def last_block(self):
        return self.chain[-1] # returns most recent block in the chain

# For testing
t1 = "Test 1"
t2 = "Test 2"
t3 = "Test 3"
t4 = "Test 4"
t5 = "Test 5"
t6 = "Test 6"

myblockchain = BlockChain() # Creates the first block

myblockchain.create_transaction_block([t1, t2])
myblockchain.create_transaction_block([t3, t4])
myblockchain.create_transaction_block([t5, t6])

myblockchain.display_chain()