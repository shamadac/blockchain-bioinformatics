from bigchaindb_driver import BigchainDB

bdb__root_url = 'https://test.bigchaindb.com:443'
tokens = {}
tokens['app_id'] = 'e037d444'
tokens['app_key'] = '22cc48d79f9d5fcebcd2206af739014f'
database = BigchainDB('https://test.bigchaindb.com', headers=tokens)