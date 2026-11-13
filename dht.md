# Distributed Hash-Table


## Description

[Distributed hash-table](https://en.wikipedia.org/wiki/Distributed_hash_table),
or `DHT`, provides an interface similar to an associative array or dictionary of key/value pairs, where the storage of all (key, value) pairs is distributed among multiple nodes.

Because of such useful DHT characteristics as decentralization, scalability and fault tolerance, it is possible to create an integrated space for storing service information. This is an absolutely different approach, since it moves towards a distributed network infrastructure rather than common centralized client-server solutions.

Each computer running the BitDust program can be a node in the DHT network and store key/value pairs created by other users.

The BitDust software runs a DHT network based on the implementation from the [Entangled](http://entangled.sourceforge.net/) library – its source code is included in the source code of BitDust and is distributed together with it.



## Data types

Each user node uses different types of service data to interact with other computers in the network. The integrated space lets other users request any key/value pairs previously written by the user to the DHT network and get up-to-date service information.

The following is a list of records that can be written to the hash-table by each node:

* `[IDURL]` 
    user identity file source

* `[nickname]@[id-server]:address`
    external net address in [IP]:[PORT] format for receiving incoming connections

* `[nickname]@[id-server]:incoming`
    list of nodes trying to connect to the user at a given moment

* `customer_supplier:[index]:[prefix]:[version]`
    list of relations of a given customer with their suppliers



## Support BitDust network

If you agree to support other BitDust users when they are connecting to the network and would like to become a "Seed node" in the BitDust network, you can add your node to the [default_network.json](https://github.com/bitdust-io/public/blob/master/default_network.json) file which is located in the root of the BitDust public repository.

Make sure BitDust is running constantly on your machine, works reliably and is connected to the Internet.
You will be a part of the BitDust "proto-network" and receive incoming DHT requests from other nodes when they are connecting to the network for the first time.

This is how the Distributed Hash Table works - it scales well, but requires some of the nodes to be online all the time. It shouldn't create a lot of traffic on those nodes, because any other node will hit a "seed node" only once - when it joins the DHT network for the first time.

To include yourself in the list of "well-known" seed nodes, first create a fork of the [Public Git Repository](https://github.com/bitdust-io/public), modify the `default_network.json` file in your forked repository and open a [Pull Request](https://github.com/bitdust-io/public/pulls) with your changes - this way we can collaborate all together and maintain a list of the most reliable BitDust seed nodes.

Contact the BitDust contributors to let them know that you have started a new DHT node, and one of the developers will approve your Pull Request.
