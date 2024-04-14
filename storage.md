# Distributed Storage

In this section you can find information on how your data is stored within the BitDust network.

* [Introduction](#intro)
* [Suppliers / Customers](#suppliers-and-customers)
* [Upload in the Network](#upload-in-the-network)
* [Data Redundancy](#data-redundancy)
* [Download from the Network](#download-from-the-network)
* [Hardware Resources](#hardware-resources)



## Intro

The BitDust network consists out of many equal and self-governing nodes, whose owners provide a part of their hardware resources to the network. By consuming data resources from the BitDust network, users get access to a more private, secure and fully independent storage to protect their data and have the ability to chat securely with their contacts. Securly since data that is stored within the BitDust network is always encrypted.



## Suppliers and Customers 

User data allocation takes place on a fixed combination of nodes chosen beforehand, these nodes are called "suppliers". The user at the same time becomes a "customer" for all of these nodes – figuratively speaking a user "rents" a portion of the hard disk drive from each of their suppliers. However is free to "fire" any of their suppliers at any moment in time and find another supplier within the BitDust Network. 

Before the user can start their first data upload, the BitDust program on the user's device has to search and connect to the user's suppliers and request "needed space" for their data. At any time, in the program settings, a user can adjust two key parameters of their distributed storage environment:

+ a volume of "needed" space
+ a desired number of suppliers

By providing this data the system calculates the amount of space that should be provided by every node:

    <supplier quota> = ( <needed space> / <number of suppliers> ) * 2

In the formula we have to multiply final quota by 2 because of redundancy. Data, stored on sthe supplier's machine, takes twice more space than original file. In some cases it might be less, because files are compressed before they will be encrypted.

The number of suppliers you can use can be one of these values:
`2`, `4`, `7`, `13`, `18`, `26`, `64`. Further you will find a detailed description on how the data allocation is done and how the combinations of suppliers are formed.

The number of customers whom each supplier can support theoretically is not limited. However by supporting too many customers the possible sessions number can be exceeded – this parameter depends on your operation system, which runs the given BitDust node and the local network limitations.

Apart from the simultaneous upload/download from a user's machine it can happen that the network channel which each customer receives will be severely restricted – only nodes with very high bandwidth will be able to support a great number of nodes.



## Upload to the Network

Each of the suppliers receives equal portions of the total volume of uploaded user data. Each fragment of uploaded data is marked with a number of the supplier from the general combination. By changing one supplier for another the new node gets exactly the data which corresponds to his their number within the combination. 
 
For a regular and stable upload input the data is archived and divided into blocks. This phase is practically identical to the creation of a regular archive from the folder content or a file on the hard disk drive and divided by the volumes.

Afterwards each block is encrypted with one of the user's private keys. Different keys derived from your Master key is used to encrypt your data - this way you can share a given file of data with another user, more information about group access can be found in the [Data Security](security.md) section. 

Furthermore, your encrypted data will be divided into fragments of equal size, which are temporary saved on your local hard disk drive. At the final stage these local files, which are ready for sending, are uploaded oonto the remote suppliers’ nodes. There they are stored as it is (in encrypted state), but are fully distributed over the whole combination of suppliers – each supplier receives exactly those fragments which were prepared for their position within the combination. 

Here is the general sequence of actions to run a new distributed data copy of your data:

1. reading input data from the folder or file on user’s local hard disk drive 
2. data archivation and optional compression with `gzip`
3. division of unitary array of binary data into the blocks of the same size 
4. encryption of each block with one of user’s secret keys
5. starting RAID-procedures for creation of fragment combination from each block
6. forming data portions from fragments and storing temporary on the local disk drive
7. upload of all portions on the assigned suppliers’ nodes
8. deleting temporary files from the local disk drive (optional)

In the settings the user can state a maximum and desired block size for all data backups – this will influence the final portion size, which will be uploaded one by one and stored at your suppliers.

For uploading data which consist out of big blocks, the amount of loss increases critically and it can lead to low data reliability. On the other hand in case of small block sizes the total number of fragments increases and this creates influence on the overall program performance and amount of required memory on the customer machine.


## Data Redundancy

In the section [Automatic Data Rebuilding](rebuilding.md) the method of converting the input data before allocating them on the nodes of suppliers is explained in more in detail. Data uploaded within the network comes with double redundancy and is organized in a RAID array for ensuring a possibility of their recovery in the case of loss. 

There are two parallel layers which are Data and Parity. They have the same size, but have a different content:

+ The Data layer consists completely out of input data 
+ The Parity layer has modified content, built with the help of a RAID procedure

For generating a Parity layer during the backup processing data byte-wise taken and a XOR operation is applied between the Data fragments of your other suppliers. The final RAID array is organized in a way that each Parity fragment allows restoring the corresponding Data fragment onto the machine of a new supplier, which replaces the lost one.

By building a RAID array so-called ECC codes are used : these are the combinations of Data and Parity allocation on the suppliers machines. For each of the possible supplier combinations the optimal ECC code was calculated before - it basically defines the framework of the mutual bracing of the Data and Parity fragments in the layers and a maximum quantity of simultaneous errors, which may occur without block sustainability loss.



## Download from the Network

For downloading existing data from the BitDust network the software performs such steps: 

1. sending requests to download existing data fragments from suppliers
2. restore each block from the reassembled together with the fragments of data
3. decrypt each restored block and check its sustainability by e-signature
4. assemble all restored blocks in a single archive
5. extract data from the archive to the user’s hard disk drive
6. delete temporary files and archive file

In the case some of the fragments were lost, for example, due to the fault in connection of some of your suppliers, the mechanism of [data recovery](rebuilding.md) in the Data layer from the on hand fragments of Parity layer will be started - see point 2. above.


## Hardware Resources 

All nodes in BitDust network are absolutely equal in their possible roles and are self goverened. There are no dedicated servers of a higher order, having special authority, managing global processes and network structure, doing global routing, monitoring or data acquisition, etc.

Each and every user always voluntarily starts the BitDust program on own device and posses full control over the BitDust software process. So everyone will have an opportunity to consume hardware resources of other nodes from one side and also donate part of own PC resources to other users in the network. Meaning that besides being a consumer you can also fulfill a supporting role within the BitDust network, depending on your hardware. The BitDust software should take care about all operations going on on your device and all processes are/will be fully automated.

Finally hardware resources can be requested and consumed from other users by you:

+ space on the hard disk drive of your "suppliers"
+ CPU time of your "scrubbers"
+ network bandwith of your "routers"

In the program settings a user can set the following key data:

+ storage quota requested from others for own use
+ desired number of suppliers for your distributed storage

These program settings are from a users perspective. We will be working on a easy to use application for all the supporting roles within the BitDust network. You can read more about these supporting roles in the supporting roles section and how you can set them up from command line.

