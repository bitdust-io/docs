# How does it work?

To explain how the BitDust generally works there are some key aspects explained below to highlight the features of the network. 


## Fully decentralized peer-to-peer network

The entire BitDust network consists out of equal nodes, every supporting device can act as a client and server for others at same time. 
The user authorizes themselves within the network and is able to safely interact with others using their ID and a secret key.


## Distributed Data Storage

Each BitDust network user is able to allocate their data on the machines of their suppliers. 
Uploaded data is backed up and organized into a RAID array to ensure the possibility of reliable recovery. 


## Automatic Data Recovery

Each supplier gets a two types of data: the data is being stored in a encrypted form and a RAID-copy, 
which enables recovery when data is lossed. The whole process is done automatically and does not need 
any action from the user.


## User Information Protection

All service packets are digitaly signed and personal user data is also encrypted with one of their secret keys. Making sure that suppliers 
do not have access to your data. Only with a correct private key you can restore the uploaded data.


## Anonymous Network Log-On

To log on to the network it isn't required to pass through any traditional authorization meaning that you are not obligated to provide personal information of any sort (email, phone number, etc.) 
All you need is a nickname and a personal private key to log onto the network. Only you have access to your private key. There is no centralized entity within the BitDust network that stores your private key.


## Uses Distributed Hash-Table

Distributed hash-table is used for service information storage, connection between users and maintenance 
of the network as a whole.


## Transmits Data by TCP and UDP

Nodes in the BitDust network are connected to each other directly and data is transmitted using 
the protocols TCP and UDP.


## Users Connections beyond NAT

There are situations when the network connection between nodes which are behind NAT cannot be established - receive direct 
incoming connections in regular manner is not possible. In those cases a distributed hash-table for service information 
storage is used, similar to rendezvous-point principle, whereby other nodes will help you to connect to the network. 


## Managed by Finite State Machines

BitDust project is developed based on principles of automata-based programming and 
[open project documentation](http://is.ifmo.ru/articles_en/).
This is a programming paradigm in which a program or its fragment is represented as a model of 
some finite state machine.


<div class=fbcomments markdown="1">
</div>
