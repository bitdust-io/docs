# Glossary


## BitDust
Global computer network for distributed data storage, sharing, publishing, digital communications, etc.


## BitDust Program
Open-source software delivered and distributed by [BitDust contributors](https://bitdust.io/#slide-7)
under [GNU Affero General Public License v3](https://www.gnu.org/licenses/agpl-3.0.en.html).


## Node
Computer connected to the Internet, which has [BitDust Software](#bitdust-program) installed and running.


## BitDust Network
Voluntary association of people using their personal computers as independently interacting with each other [BitDust Nodes](#node).


## Data
Any information which can be stored on a computer disk drive as a single file or a folder.


## Backup Copy
Exact copy of [data](#data) encrypted by some [node](#node), which was created at some point in time.


## Folder Backup Copy
[backup copy](#Backup-copy) of data, which was obtained from archiving all files stored in the given folder on computer hard disk drive, possibly including also all sub-folders.


## Distributed Copy
A [backup copy](#backup-copy), which was stored on different [nodes](#node) in [BitDust network](#bitdust-network).


## Block
A file on a hard disk drive containing only a part of [backup copy](#backup-copy) and having an order number, assigned at the moment of creation.


## Fragment
A part of [block](#block), prepared in the process of a [backup copy](#backup-copy) creation and having an order number – position in the block, also may be called as sector.


## Size of Backup Copy
Total size of all [blocks](#block) related to given [backup copy](#backup-copy).


## Packet
## Service Packet
Useful information transferred from one [node](#node) to another in the [BitDust network](#bitdust-network)
and containing [digital-signature](#digital-signature) of the sender.


## Data Packet
## Data Portion
A [packet](#packet), containing [encrypted](#encryption) [fragment](#fragment) of [data](#data).


## BitDust Data Storage
A method of [data](#data) processing which implies source data [encryption](#encryption),
[archivation](#archivation) and relocation on different [nodes](#node),
divided into [blocks](#block) and [fragments](#fragment).


## Recovery
A process of inverse transformation of [data](#data) from divided [fragments](#fragment) and source data reconstruction from existing [backup copy](#backup-copy).


## Upload to the BitDust Network
A process of creation of [distributed copy](#distributed-copy) of given [data](#data),
[portions](#data-portion) of which are located at [suppliers](#supplier) machines.


## Download from the BitDust Network
A process of [data](#data) [recovery](#recovery) from 
[distributed copy](#distributed-copy),
which was initially located at the [suppliers](#supplier) machine.


## Supplier
A [node](#node) in the [BitDust network](#bitdust-network), whose owner voluntary agreed to store other user's [data](#data) on the hard disk drive of his personal computer.


## Client
A [node](#node) in the [BitDust network](#bitdust-network), whose owner uses the space on the HDD's of other [nodes](#node) for storing his own [data](#data).


## Clients Folder
A local folder on the hard disk drive of the [supplier](#supplier) machine, 
where [data](#data) of his [clients](#client) are stored.


## Shared Supplier Space
Maximum possible volume reached by [clients folder](#clients-folder).


## Used Supplier Space
Current volume of [clients folder](#clients-folder).


## Allocated Client Space
A byte value previously agreed upon with the user, which states the maximum total volume of all [data](#data), that the [client](#client) can locate at the given [node](#node).


## Free Supplier Space 
A difference between [shared supplier space](#shared-supplier-space) and total volume of [allocated client space](#allocated-client-space) for all the [clients](#client) of the user.


## Used Client Space
Total volume of all already created [distributed copies](#distributed-copy) of the given user.


## Requested Client Space
An upper bound of [used client space](#used-client-space)
for given user – in other words a maximum total volume of [data](#data), which can be allocated at the [suppliers](#supplier).


## Free Client Space
A difference between [requestd](#requested-client-space) and 
[used](#used-client-space) [clients](#client) space.


## Command
A [packet](#packet) of [data](#data) containing only code phrase, a [message](#message) or any other information, used for interaction between [nodes](#node) in the [BitDust network](#bitdust-network).


## Message
[encrypted](#encryption) text message addressed at exact user. 


## Encryption
Some [data](#data) transform for the purpose of its protection.


## Archivation
[data](#data) transform for the purpose of creating a unified stream and decreasing the total size of the stored information, 


## Public Key
## Private Key
## Digital signature
Secret key is used for personal data protection, you are welcome to read 
[detailed article](http://ru.wikipedia.org/wiki/%d0%9a%d1%80%d0%b8%d0%bf%d1%82%d0%be%d1%81%d0%b8%d1%81%d1%82%d0%b5%d0%bc%d0%b0_%d1%81_%d0%be%d1%82%d0%ba%d1%80%d1%8b%d1%82%d1%8b%d0%bc_%d0%ba%d0%bb%d1%8e%d1%87%d0%be%d0%bc)
on Wikipedia.


## Identity
A publicly readable file containing an [public key](#public-key), 
[digital-signature](#digital-signature), contact details and other information belonging to exact user.


## ID-server
## Identity server
A single [node](#node) in the [BitDust network](#bitdust-network) which acts as a server receiving and storing [identity](#identity) files for other nodes.


## Identity URL
## IDURL
## User Identifier
Uique address of the exact [identity](#identity) file in the Internet and [BitDust network](#bitdust-network).


## Network Logon
A process of creating a new [identity](#identity) file, its sending to several [id-servers](#id-server) and receiving unique [IDURL](#idurl) address for given user.


## Identity Recovery
A process of downloading of [identity](#identity) file from one of the [id-servers](#id-server) ( via known [IDURL](#idurl) ) and further conformance check of file content and user [private key](#private-key). 


## Automation
## Finite State Machine
A mathematical model designed for specification of any algorithm in which all possible [states](#state) of the prototype process are salient and transitions between states are specified.


## State
One of the stages of the algorithm, which were allocated logically reasonable analysis of the simulated process.


## Transition Graph
Visual framework of the [finite state machine](#finite-state-machine) which displays: states, transitions, events, conditions, actions and text descriptions.

