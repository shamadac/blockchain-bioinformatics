    # -*- coding: utf-8 -*-

from . import database
import bigchaindb_driver
from time import sleep
from sys import exit

def register(ID, unique_id, public_key, private_key, asset_type=""):
    
    # Define asset payload
    user = {
            'data': {
                'user': {
                        'id': unique_id,
                        'public_key': public_key,
                        'private_key': private_key,
                },
            },
    }
    
    # Create digital asset
    prepared_tx = database.transactions.prepare(
            operation='CREATE',
            signers=public_key,
            asset=user,
    )
    
    # Fulfill and send transaction
    fulfilled_tx = database.transactions.fulfill(
            prepared_tx,
            private_keys=private_key
    )
    sent_tx = database.transactions.send(fulfilled_tx)
    
    txid = fulfilled_tx['id']  # Store transaction ID
    
    # Check status of transaction
    trials = 0
    
    while trials < 100:
        try:
            if database.transactions.status(txid).get('status') == 'valid':
                print("Asset (%s) is registered on the blockchain." % asset_type)
                break
        except bigchaindb_driver.exceptions.NotFoundError:
            trials += 1
            sleep(1)
    
    if trials == 100:
        print('Tx is still being processed...Check again later.')
        exit(0)
    
    # Retrieve validated transaction
    tx_retrieved = database.transactions.retrieve(prepared_tx['id'])