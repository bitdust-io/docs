# How does it work?

To explain how the BitDust generally works there are some key aspects explained below to highlight the features of the network. 


## Fully decentralized peer-to-peer network

The entire BitDust network consists out of equal nodes, every supporting device can act as a client and server for others at same time.

The user authorizes themselve within the network and is able to safely interact with others using their ID and own private key.


## Distributed Data Storage

Each BitDust user is able to allocate data on the machines of other users - those are called suppliers.

Uploaded data is encrypted first and then backed up and organized into a RAID array to ensure the possibility of reliable recovery.


## Automatic Data Recovery

Each supplier gets a two types of data: the data is being stored in a encrypted form and a RAID-copy,
which enables recovery when data is lossed. The whole process is done automatically and does not need
any action from the user.


## User Information Protection

All service packets are digitaly signed and personal user data is also encrypted with one of the secret keys. Making sure that suppliers or other
unauthorized users do not have access to your data. Only with a valid private key you can restore the uploaded data or read the incoming message.


## Anonymous Network Log-On

To log on to the network it isn't required to pass through any traditional authorization meaning that you are not obligated to provide personal information of any sort (your name, address, email, phone number, etc.)

All you need is a nickname and a personal private key to log onto the network. Only you have access to your private key because it is generated directly on your device
when you start the software for the first time. There is no centralized entity within the BitDust network that stores your private key.


## Uses Distributed Hash-Table

Distributed hash-table is used for service information storage, supporting connection between users and maintenance of the network as a whole.


## Transmits Data by HTTP, TCP or UDP

Nodes in the BitDust network are connected to each other directly and data is transmitted using your active Internet connection.


## Users Connections beyond NAT

There are situations when the network connection between nodes which are behind NAT cannot be established in a peer-to-peer way - receiving direct
incoming connections in regular manner is not always possible in the Internet era. In those cases a other nodes, called proxy-routers, are used to route the traffic.


## Managed by Finite State Machines

BitDust project is developed based on principles of automata-based programming and 
[open project documentation](http://is.ifmo.ru/articles_en/).
This is a programming paradigm in which a program or its fragment is represented as a model of 
some finite state machine.

