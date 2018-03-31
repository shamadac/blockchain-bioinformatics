#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Import modules
import bigchaindb_driver

from bigchaindb_driver.crypto import generate_keypair
from time import sleep
from sys import exit

# Create instance of BigChainDB



# Digital asset definition
docker = {
        'data': {
            'docker': {
                    'id': 'reallyawesomedocker',
                    'developer': 'user1'
            },
        },
}

# Generate keypairs
user1, user2 = generate_keypair(), generate_keypair()

# Create digital asset
prepared_asset_tx = database.transactions.prepare(
        operation='CREATE',
        signers=user1.public_key,
        asset=docker,
)

# Fulfill and send transaction
fulfilled_asset_tx = database.transactions.fulfill(
        prepared_asset_tx,
        private_keys=user1.private_key
)
sent_asset_tx = database.transactions.send(fulfilled_asset_tx)

print(sent_asset_tx == fulfilled_asset_tx)    # Test

txid = fulfilled_asset_tx['id']  # Store transaction ID

# Check status of transaction
trials = 0

while trials < 100:
    try:
        if database.transactions.status(txid).get('status') == 'valid':
            print("Asset is registered on the blockchain.")
            break
    except bigchaindb_driver.exceptions.NotFoundError:
        trials += 1
        sleep(1)

if trials == 100:
    print('Tx is still being processed...Check again later.')
    exit(0)

# Retrieve validated transaction
tx_retrieved = database.transactions.retrieve(prepared_asset_tx['id'])

# Prepare transfer transaction
asset_tx = fulfilled_asset_tx
asset_id = asset_tx['id']
transfer_asset = {
        'id': asset_id
}

output_index = 0
output = asset_tx['outputs'][output_index]

transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
                'output_index': output_index,
                'transaction_id': asset_tx['id']
        },
        'owners_before': output['public_keys']
}

prepared_transfer_tx = database.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=user2.public_key
)

# Fulfill and send transaction

fulfilled_transfer_tx = database.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=user1.private_key
)

sent_transfer_tx = database.transactions.send(fulfilled_transfer_tx)

if sent_transfer_tx['inputs'][0]['owners_before'][0] == user1.public_key and sent_transfer_tx['outputs'][0]['public_keys'][0] == user2.public_key:
       print("Asset successfully transferred from User1 to User2.")

# Creating divisible asset
docker_rights = {
        'data': {
            'rights_to': {
                    'docker': {
                            'id': 'reallyawesomedocker',
                            'developer': 'user1'
                            }
                        },
            'description': 'Rights to assets. 100 rights to be shared.',
                },
}

developer = generate_keypair()
customer = generate_keypair()

prepared_rights_tx = database.transactions.prepare(operation = 'CREATE', signers = developer.public_key, recipients = [([developer.public_key], 100)], asset = docker_rights)

fulfilled_rights_tx = database.transactions.fulfill(prepared_rights_tx, private_keys = developer.private_key)

sent_rights_tx = database.transactions.send(fulfilled_rights_tx)

txid = fulfilled_rights_tx['id']

trials = 0
while trials < 100:
    try:
        if database.transactions.status(txid).get('status') == 'valid':
            print("Developer successfully created 100 rights for docker, and assigned them to themselves.")
            break
    except bigchaindb_driver.exceptions.NotFoundError:
        trials += 1
        sleep(1)
if trials == 100:
    print('Tx is still being processed...Check again later.')
    exit(0)

developer_rights = fulfilled_rights_tx['outputs'][0]['amount']


print(developer_rights)