# Python Blockchain

This project is intended as a learning tool to understand the fundamentals of blockchain. It is a proof-of-work blockchain client loosely based on Bitcoin, with a number of major simplifications to make it easier to read (see [Limitations](#limitations)). 

### Prerequisites

 - Python 3
 - Docker (assuming you don't just have a Redis instance lying around)
 
### Running

First, you'll need to spin up a redis instance.

```ps
docker pull redis
docker run -p 6379:6379 --name my-redis -d redis
```

Next, you'll need to update settings.py to point to a valid, passwordless [RSA public/private key](https://www.vultr.com/docs/how-do-i-generate-ssh-keys) pair.

```python
...
PRIVATE_KEY_FILE = "C:\\Users\\MYUSERNAME\\.ssh\\id_rsa"
PUBLIC_KEY_FILE = "C:\\Users\\MYUSERNAME\\.ssh\\id_rsa.pub"
```

Now you can spin up a node.

```ps
python .\app.py
```

To spin up another node, clone the repo to another location (so that you have a fresh settings.py file), point settings.py to a *different* public/private key pair, and run that app.py.

Once your node has mined a block or two, you can spend your block reward by sending a transaction.

```ps
python .\send.py 1 RecepientPublicKey
```

Finally, when you are ready to close everything out, kill the nodes (they may take a minute to exit gracefully) and shutdown the Redis container.

```ps
docker stop my-redis
docker container prune -f
```

### Limitations

Compared with most other blockchains, this one currently has the following limitations (either for readability, or because I haven't built it yet):

 - There is no concept of contract scripting (e.g. Bitcoin Script, Ethereum Solidity). Transactions simply send a quantity to a given public key.
 - The mining block reward is hardcoded, and does not [decrease as the chain lengthens](https://www.bitcoinmining.com/what-is-the-bitcoin-block-reward/).
 - The difficulty is hardcoded, and does not [scale based how fast the network mines blocks](https://en.bitcoin.it/wiki/Difficulty).
 - Transactions do not support multi-input/multi-output. This means each transaction must send the entire balance of the input transaction. Since the mining reward is hardcoded to 1, this means every transaction must send exactly 1.
 - There is no concept of a transaction fee.
 - RSA public/private keys are used instead of [a base58 of a RIPEMD160 of a SHA256 of a ECDSA key](https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses).
 - Redis pub/sub is used to broadcast messages to other nodes in place of a true p2p network.
 - It is written in python.
 
### Further reading

Here are some resources I have found useful learning about blockchains:

 - A really good [blockchain introduction](https://marmelab.com/blog/2016/04/28/blockchain-for-web-developers-the-theory.html). My favorite is the part where the author says ["you won't build your own blockchain"](https://marmelab.com/blog/2016/04/28/blockchain-for-web-developers-the-theory.html#you-wont-build-your-own-blockchain).
 - Why most cryptocurrencies use [ECDSA keys](https://crypto.stackexchange.com/questions/3216/signatures-rsa-compared-to-ecdsa)
 - P2P networks are [really complicated](http://chimera.labs.oreilly.com/books/1234000001802/ch06.html)
 - Some other interesting blockchain implementations are [Etherium](https://github.com/ethereum/wiki/wiki/White-Paper) and [Hyperledger Fabric](https://hyperledger.org/projects/fabric)