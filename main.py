"""
A blockchain, which is a decentralized digital ledger where transactions are recorded.
The data is immutable (cannot be changed) and is distributed across multiple devices.
This blockchain will track the path of pharmaceutical products.
This is a real world application, since pharmaceuticals can sometimes be spiked with fentanyl or carry diseases.
"""

import hashlib # The hash library provides secure hash functions that let you create hashes or message digests of data.
import csv # Allows for comma-separated values files (e.g., Excel Spreadsheets)
import json # Allows you to work with JavaScript Object Notation, a lightweight data format used for storing and exchanging data
import time # Time-related functions
import os # Provides functions for interacting with the operating system (e.g., checking if a file exists)

class Block: # Creates a block with its own unique hash using the transaction data and previous hash
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index # the position of the block in the chain
        self.timestamp = timestamp # the time the block was created
        self.data = data # data: information about the pharmaceutical event (e.g., shipment, location)
        self.prev_hash = prev_hash # hash of the previous block (used to link blocks securely)

        # stores the block's content in dictionary form so it can be easily hashed or displayed
        self.block_info = {
            "Index": self.index,
            "Timestamp": self.timestamp,
            "Data": self.data,
            "Previous Hash": self.prev_hash
        }
        self.hash = self.calcHash()

    def calcHash(self):
        """
        * Converts the dictionary into a JSON-formatted string — a standardized way to represent data.
           - dumps = "dump to string"
           - sorts_keys=True ensures dictionary keys are always in the same order, which is crucial since
             hashing is highly sensitive (even the smallest difference will interfere with the hash)
           - .encode() turns the string into bytes, which is what the hashing function needs as input
        """
        block_str = json.dumps(self.block_info, sort_keys=True).encode() #
        return hashlib.sha256(block_str).hexdigest() # generates a hash using Secure Hash Algorithm 256-bit

class PharmaBlockChain:
    def __init__(self):
        self.chain = [self.generate_genesis_block()] # holds all the blocks

    def generate_genesis_block(self): # first block, serves as a starting point.
        # Uses "0" as previous hash since no previous block exists
        return Block(0,time.ctime(), {"Event": "Genesis Block"}, "0")

    def retrieve_block(self):
        # retrieves the latest block, which is needed to link the next new block to the correct previous hash
        return self.chain[-1]

    def create_block(self, data): # adds new block to the chain
        last_block = self.retrieve_block()

        # create a new block linked to the last one
        new_block = Block(
            index=last_block.index + 1,
            timestamp=time.ctime(),
            data=data,
            prev_hash=last_block.hash
        )
        self.chain.append(new_block)

    def validation(self): # determines if the block is valid
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.prev_hash != previous_block.hash: # if the block's hash doesn't match the previous hash
                print(f"Block {i} has been tampered with")
                return False
        return True

    def write_chain(self, ledger_path): # writes to a CSV file
        """
        Writes the blockchain's contents to a CSV file.
        If the file doesn't exist, a new one is created
        If the file is empty, or is missing a header, a header is written first.
        """
        header_needed = False

        # Check if file is missing or empty
        if not os.path.exists(ledger_path) or os.stat(ledger_path).st_size == 0:
            header_needed = True
        else:
            # If file exists, check the first line for correct header
            with open(ledger_path, "r") as csv_ledger:
                first_line = csv_ledger.readline()
                if "Timestamp" not in first_line:
                    header_needed = True

        # Open the file in append mode
        with open(ledger_path, "a", newline="") as csv_ledger:
            appender = csv.writer(csv_ledger)

            # Write the header if necessary
            if header_needed:
                appender.writerow(["Timestamp", "Data", "Hash"])

            # Write each block's data into the CSV
            for block in self.chain:
                # Serialize the data dictionary into a readable string (like JSON) for CSV storage
                data_string = json.dumps(block.data, sort_keys=True)
                appender.writerow([block.timestamp, data_string, block.hash])

    def display_chain(self): # displays all the data within each block, including their hash values
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Event: {block.data.get('event', 'N/A')}")
            print(f"Batch ID: {block.data.get('batch_id', 'N/A')}")
            print(f"Location: {block.data.get('location', 'N/A')}")
            print(f"Destination: {block.data.get('destination', 'N/A')}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.prev_hash}")

    @property # decorator, turns a method into a read-only attribute
    def last_block(self):
        return self.chain[-1] # returns most recent block in the chain

ledger = "my_ledger.csv"

myblockchain = PharmaBlockChain() # Creates the first block

# Simulating a real pharmaceutical product journey through the supply chain
#1 Manufactured
myblockchain.create_block({
        "event": "Manufactured",
        "batch_id": "Batch 1",
        "location": "Factory A",
        "destination": "Distributor 1"})

#2 Quality test
myblockchain.create_block({
    "event": "Quality Tested",
    "batch_id": "Batch 1",
    "location": "Testing Lab A",
    "destination": "Distributor 1"})

#3 Shipped to Distributor
myblockchain.create_block({
    "event": "Shipped",
    "batch_id": "Batch 1",
    "location": "Factory A",
    "destination": "Distributor 1"
})

#4 Received by Distributor
myblockchain.create_block({
    "event": "Received",
    "batch_id": "Batch 1",
    "location": "Distributor 1",
    "destination": "Warehouse X"
})

#5 Shipped to Pharmacy
myblockchain.create_block({
    "event": "Shipped",
    "batch_id": "Batch 1",
    "location": "Warehouse X",
    "destination": "CVS Pharmacy"
})

#6 Received by Pharmacy
myblockchain.create_block({
    "event": "Received",
    "batch_id": "Batch 1",
    "location": "CVS Pharmacy",
    "destination": "CVS Pharmacy"
})

#7 Sold to Customer
myblockchain.create_block({
    "event": "Sold",
    "batch_id": "Batch 1",
    "location": "Pharmacy X",
    "destination": "End User"
})


myblockchain.write_chain(ledger)
myblockchain.display_chain()

#Tampered Block (Invalid): creates a block with a wrong previous hash to simulate tampering
# This simulates data tampering, which should be detected during validation
# This will not be written to the CSV file
tampered_block = Block(
    index=myblockchain.last_block.index + 1,
    timestamp=time.ctime(),
    data={
        "event": "Mugged after purchase",
        "batch_id": "Batch 1",
        "location": "Dark alleyway",
        "destination": "Albuquerque, New Mexico"
    },
    prev_hash="WhatAreTheOdds"  # Wrong previous hash
)

myblockchain.chain.append(tampered_block)
is_valid = myblockchain.validation()
print(f"\nBlockchain Validity: {is_valid}")