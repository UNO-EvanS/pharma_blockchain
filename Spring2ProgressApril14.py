"""
A blockchain, which is a decentralized digital ledger where transactions are recorded.
The data is immutable and is distributed across multiple devices.
This blockchain will track the path of pharmaceutical products.
This is a real world application, since pharmaceuticals can sometimes be spiked with fentanyl or carry diseases.
"""

import hashlib, csv, json, time

class Block: # Creates a block with its own unique hash using the transaction data and previous hash
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash # ensures blocks remain linked together

        self.block_info = {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Data": self.data,
            "Previous Hash": self.prev_hash
        }
        self.hash = self.calcHash()

    def calcHash(self):
        # Creates a hash of the block's contents
        block_str = json.dumps(self.block_info, sort_keys=True).encode()

        return hashlib.sha256(block_str).hexdigest() # generates a hash using Secure Hash Algorithm 256-bit

class PharmaBlockChain:
    def __init__(self):
        self.chain = [self.generate_genesis_block()] # holds all the blocks

    def generate_genesis_block(self): # first block
        return Block(0,time.ctime(), {"Event": "Genesis Block"}, "0")

    def retrieve_block(self): # retrieves latest block
        return self.chain[-1]

    def create_block(self, data): # adds new block to the chain
        last_block = self.retrieve_block()
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.ctime(),
            data=data,
            prev_hash=last_block.hash
        )
        self.chain.append(new_block)

    def validation(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.prev_hash != previous_block.hash:
                print(f"Block {i} has been tampered with")
                return False

            if current_block.prev_hash != previous_block.hash:
                print(f"Block {i}'s previous hash does not match")
                return False

        return True


    def write_chain(self, ledger_path):
        try:
            with open(ledger_path, "a", newline="") as csv_ledger:
                appender = csv.writer(csv_ledger)
                appender.writerow(["Data", "Hash"])
                for i in range(len(self.chain)):
                    appender.writerow([i + 1, self.chain[i].data])

        except FileNotFoundError as f:
            with open(ledger_path, "w", newline="") as csv_ledger:
                writer = csv.writer(csv_ledger)
                writer.writerow()



    def display_chain(self): # displays all the data within each block, including their hash values
        for block in self.chain:
            print(f"\nBlock #{blocmain.pyk.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Event: {block.data.get('event', 'N/A')}")
            print(f"Batch ID: {block.data.get('batch_id', 'N/A')}")
            print(f"Location: {block.data.get('location', 'N/A')}")
            print(f"Destination: {block.data.get('destination', 'N/A')}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.prev_hash}")

    @property
    def last_block(self):
        return self.chain[-1] # returns most recent block in the chain

ledger = "my_ledger.csv"

myblockchain = PharmaBlockChain() # Creates the first block

# Samples for testing
test1 = myblockchain.create_block({
        "event": "Manufactured",
        "batch_id": "Batch 1",
        "location": "Factory A",
        "destination": "Distributor 1"})


myblockchain.write_chain(ledger)

myblockchain.display_chain()