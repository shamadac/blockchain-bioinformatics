# blockchain-bioinformatics
Hack Schulich 2018

Hello team! Man learning how to make a github repo was not easy...

So I just committed the framework for a django project called "blockchain_bioinformatics" with an app called "DockerMarket".

To recap:
  - django (djangoproject.com) is a web framework for python; it makes it easy to model data structures, pass information between the front and back ends, and interact with data using python. The directories and files initially committed are what is automatically generated when you create a new django project and then create an app within that project. In the future, if we choose to continue with this project, we can create new apps within blockchain_bioinformatics (eg. we could also make a "GWAS Market").

  - BigchainDB is an easy and intuitive framework for creating and transacting digital assets on a blockchain network. the BigchainDB blockchain nodes run complete MongoDB (and/or RethinkDB) servers, allowing for large amounts of data to be stored on the network. This means we can define bioinformatics data and/or pipelines (Docker, as BJ will explain) as a digital asset class and allow users to register such assets on the blockchain (I believe BigchainDB operates on the Ethereum blockchain, but I am not entirely sure. That said, Ethereum can be used to tokenize the market later, but we don't need to take this project that far for the hackathon). When users do this, they will retain ownership of their data and/or pipelines and be compensated by anyone using these assets in a peer-to-peer manner. You can install the BigchainDB Python driver and its dependencies here (https://docs.bigchaindb.com/projects/py-driver/en/latest/quickstart.html)
  
  - Once you have both python packages (BigchainDB & django), we can use django for a client-facing website, and BigchainDB for the processing of transactions and storage of the assets themselves. Both django and BigchainDB will provide queryable databases; we can store user-relevant data on the web-host server (django lets us choose from different engines, including mySQL), and the asset-relevant data on BigchainDB (ie user's public & private keys and asset payloads). Since everything is in Python, we should be able to easily build the BigchainDB scripts into the django code.
  
  - For instance, this is what it might look like:
    - A user (presumably a scientist) registers an account on the website. When they submit their user data, backend scripts register the user data on both the web-host databases (eg mySQL) as well as on BigchainDB (and makes a public & private key set).
    - This user can then submit a bioinformatics data-set or pipeline, which will be registered (in the backend) as a digital asset on BigchainDB, and a reference key of some sort to the BigchainDB entry will be stored on the web-host mySQL.
    - Another user can then use this data/pipeline, but in doing so, the backend will move some "funds" from this user's private key to that of the data/pipeline owner.
