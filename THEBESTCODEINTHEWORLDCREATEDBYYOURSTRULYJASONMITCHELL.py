import hashlib
import json
import random
import time
from datetime import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None,
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        if sender not in wallet_balances:
            print(f"Sender {sender} not found in wallet balances. Transaction failed.")
            return -1

        if wallet_balances[sender] < amount:
            print(f"Sender {sender} does not have enough balance to send {amount} ETH. Transaction failed.")
            return -1

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

def save_data():
    data = {
        "wallet_balances": wallet_balances,
        "transactions": transactions
    }
    with open("blockchain_data.json", "w") as file:
        json.dump(data, file)

def load_data():
    try:
        with open("blockchain_data.json", "r") as file:
            data = json.load(file)
            return data.get("wallet_balances", {}), data.get("transactions", [])
    except FileNotFoundError:
        return {}, []

ethereal_wallets = [f"0xWallet{i}" for i in range(1, 6)]
wallet_balances, transactions = load_data()

# Initialize wallet balances with non-zero values
for wallet in ethereal_wallets:
    wallet_balances.setdefault(wallet, round(random.uniform(1, 100), 2))

blockchain = Blockchain()

print("Welcome to Ethereal Blockchain Simulator!")
while True:
    print("\nMenu:")
    print("1. Simulate Ethereal Transactions")
    print("2. Display Wallet Balances and Transactions")
    print("3. Display Blockchain")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        num_transactions = int(input("Enter the number of transactions you want to simulate: "))

        for _ in range(num_transactions):
            print("\nAvailable Wallets with Balances:")
            for i, wallet in enumerate(ethereal_wallets):
                print(f"{i + 1}. {wallet}: {wallet_balances.get(wallet, 0)} ETH")

            sender_index = int(input("Enter the sender's wallet number (1 to 5): ")) - 1
            receiver_index = int(input("Enter the receiver's wallet number (1 to 5, different from sender): ")) - 1

            if sender_index == receiver_index or not (0 <= sender_index < len(ethereal_wallets)) or not (0 <= receiver_index < len(ethereal_wallets)):
                print("Invalid input. Sender and receiver must be different and within the range.")
                continue

            eth_amount = round(float(input("Enter the ETH amount to send: ")), 2)
            sender = ethereal_wallets[sender_index]
            receiver = ethereal_wallets[receiver_index]

            if wallet_balances.get(sender, 0) < eth_amount:
                print(f"Insufficient balance in {sender}'s wallet. Transaction canceled.")
                continue

            print(f"Simulating Ethereal Transaction: {sender} -> {receiver}, Amount: {eth_amount} ETH")

            transactions.append((sender, receiver, eth_amount))
            wallet_balances[sender] = wallet_balances.get(sender, 0) - eth_amount
            wallet_balances[receiver] = wallet_balances.get(receiver, 0) + eth_amount
            blockchain.new_transaction(sender, receiver, eth_amount)
            save_data()
            time.sleep(1)

        print("Transactions simulated successfully!")

    elif choice == "2":
        print("\nWallet Balances:")
        for wallet, balance in wallet_balances.items():
            print(f"{wallet}: {balance} ETH")

        print("\nRecent Transactions:")
        for i, transaction in enumerate(transactions[-5:], start=1):
            sender, receiver, amount = transaction
            print(f"{i}. Sender: {sender}, Receiver: {receiver}, Amount: {amount} ETH")

    elif choice == "3":
        print("\nBlockchain:")
        for block in blockchain.chain:
            print(f"Block {block['index']}:")
            print(f"- Timestamp: {datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"- Previous Hash: {block['previous_hash']}")
            print(f"- Proof: {block['proof']}")
            print(f"- Transactions:")

            for transaction in block['transactions']:
                print(f"  - Sender: {transaction['sender']}")
                print(f"  - Receiver: {transaction['recipient']}")
                print(f"  - Amount: {transaction['amount']} ETH")

    elif choice == "4":
        print("Thank you for using Ethereal Blockchain Simulator! Goodbye.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3/4).")
