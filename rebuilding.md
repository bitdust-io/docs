# Automatic Rebuilding

In this section we describe the methods of automatic data rebuilding.

Note that at the moment automatic data rebuilding is performed by the BitDust software on the customer's own device - it works only while the software is running and connected to the network. In the future we plan to delegate this work to other nodes of the network, which will act in a supporting role called the ReBuilder - this role is not implemented yet.

In this section we cover the following items:

* [Data Redundancy](#data-redundancy)
* [RAID Transformation](#raid-transformation)
* [ECC codes](#ecc-codes)
* [Reassembly](#rebuilding)
* [Supplier Change](#supplier-change)
* [Suppliers Search](#suppliers-search)


## Data Redundancy 

In the section [Distributed Storage](storage.md) we described the mechanism of creating distributed copies of user data in the BitDust network. In this article we describe a method of partitioning data into separate fragments, which enables dynamic rebuilding when data is lost and further redistribution of that data to more reliable nodes within the network.

Data uploaded to the user's suppliers is stored with double redundancy and organized into a RAID array, so that it can be rebuilt when lost.

The storage is organized in the following way: 

+ the first layer contains input data and is called "Data" 
+ the second layer has the same size but modified content and is called "Parity"


## RAID Transformation 

Different combinations of Parity fragments enable Data fragment recovery on the machine of a new supplier that has recently replaced a previous supplier that went offline. The Parity fragments of each block are created by performing an XOR operation on each byte between several Data fragments of this block and are prepared for other suppliers.

When one or more suppliers are lost, we can still restore the missing Data fragments from the fragments downloaded from other suppliers. When this is initiated, we need to perform an XOR operation on each byte between the available Parity and Data fragments once again.

The so-called iterative algorithm continues working as long as it can restore at least one lost fragment per cycle. For example, recovering a Data fragment in one position on the first iteration allows restoring the Parity parts in other positions in the next cycle, and then Data fragments will be restored in a third position, etc.


## ECC Codes

When building a RAID array, so-called ECC codes are used – these are the best combinations of positions of Data and Parity fragments among the suppliers. Here "position" defines which fragments must be kept by a given supplier.

For each of the possible combinations of suppliers the optimal ECC code was calculated – it defines the framework of the mutual bracing of Data and Parity fragments in the layers and the maximum number of simultaneous errors that may occur without losing the block. Here you can see the allowable number of possible losses for each of the possible combinations of suppliers:


| **ecc code**              | **number of suppliers**       | **maximum errors**        |
|---:|:---:|:---:|
| ecc/64x64                 | 64                            | 10                        | 
| ecc/26x26                 | 26                            | 6                         |
| ecc/18x18                 | 18                            | 5                         |
| ecc/13x13                 | 13                            | 4                         |
| ecc/7x7                   | 7                             | 3                         |
| ecc/4x4                   | 4                             | 2                         |
| ecc/2x2                   | 2                             | 1                         |


Thus the percentage of possible losses is 50% for 2 suppliers and about 15% for 64 suppliers. The greater the number of possible errors you can have, the more time you have to reassemble the lost fragments and the more stable the data storage is. In essence, more suppliers should theoretically give you more reliable storage. But the greater the number of suppliers you use, the more memory and network connections are required from your local operating system.


### ATTENTION!

    By exceeding the number of possible errors, you should expect complete
    loss of the uploaded data. The mechanism of automatic data rebuilding
    allows swiftly fixing encountered errors and enables
    redistribution of data to reliable suppliers’ nodes.

    The BitDust team is never responsible for suppliers that go offline and also never responsible when data is lost.



## Rebuilding

The algorithm of dynamic data rebuilding cyclically runs a sequence of actions aimed at constantly maintaining a state in which data can be downloaded from the network. Currently this algorithm is executed by the BitDust software on the customer's device. In the future it will become the main responsibility of the ReBuilder supporting role (not implemented yet).

In each algorithm iteration the BitDust software will make a decision about your suppliers based on previously collected statistical data and the current connection status. The least "reliable" supplier can be fired and another random node can be found in the BitDust network to replace them.

After the supplier is changed, the fragments that were allocated on the old node are lost. Right away the software starts the "rebuilding" process to reassemble these fragments on the customer's local computer and, upon completion, places them on the new node. Based on your ECC mode and number of suppliers a set of data fragments will be downloaded upfront from other suppliers that are available at the moment.

At each iteration of the rebuilding algorithm one single block of your data is reassembled: the software puts it in a temporary folder on the local disk, arranges the network delivery to a remote supplier node and removes those fragments afterwards.

To rebuild one lost fragment the software needs to combine the Data and Parity fragments from reliable nodes and run the RAID process on that set. This takes some CPU time, because it involves huge amounts of XOR'ing in total - multiple times per each and every byte of your data. In the future, when this work is delegated to the ReBuilders, it will be important for a node acting as a ReBuilder to have the right hardware capable of performing the XOR'ing process.

The order of data assembly is determined by the creation time of each copy – the software first restores the most recently uploaded data and then sends it to reliable suppliers. BitDust keeps track of all running uploads and downloads and also "remembers" pending requests. 

The total time of the rebuilding process depends on the total size of your uploads, CPU frequency and network bandwidth limit.
Currently we have implemented a very basic scenario in which only one active upload/download process is running and all jobs are organized in a queue.

Here is a short representation of the common sequence of actions at each iteration:


1. a decision on supplier change is made – the least "reliable" node in the current supplier set is identified
2. a global network lookup finds a node that is ready to become a new supplier for the user
3. the process of downloading already allocated data fragments from other suppliers is launched
4. for each block a RAID procedure is run to recover the fragments lost with the old node
5. restored fragments are uploaded to the computer of the new supplier
6. after successful upload the restored fragments are deleted from the local disk drive (optional)
7. the rebuilding loop restarts from step 3 - the next uploaded file will be taken from the queue to be rebuilt


## Supplier Change

The key point in the mechanism of automatic data rebuilding is the method of identifying and replacing a bad supplier. After the decision is made, the software starts the rebuilding process and places the restored fragments on a new supplier. Currently the decision and the rebuilding are both done on the customer's device - in the future the rebuilding work is planned to be delegated to the ReBuilders.

The chosen ECC code determines the number of errors in the RAID array you can handle - in other words, the number of fragments that can be missing in each block while you can still reassemble the whole block.

At each iteration of the automatic rebuilding algorithm, the number of currently connected suppliers is estimated and compared with the possible number of losses for the given ECC method. If the number of inactive suppliers becomes critical, one or several suppliers are immediately replaced automatically, and the reassembly of all uploaded data and its transfer to the new nodes begins.

At the moment these methods are implemented on a basic level and need further development for optimal decision making. However, this requires a real environment for testing, and we need a greater number of real users who dynamically log on and off the network to optimize the future solution. For now we are thinking about the best starting point to move on from there.

In the future we plan to improve this functionality so that it could "predict" beforehand, based on previously collected daily/weekly statistics, who will go offline and needs to be replaced.

In the future we also plan to create conditions for external rating of suppliers who provide reliable data storage. This feature still has to be worked out, and of course the roadmap is open to change.


## Suppliers Search

Supplier change and the search for a new node in the BitDust network are done based on these parameters:

+ the volume of space requested from the network
+ the number of suppliers in the combination – it depends on the chosen ECC method

For this the distributed hash-table is queried and a random node is chosen. Then the software connects to this node and sends it a request to provide a data storage service for the user. If the request is accepted, the chosen node becomes a new supplier for that user. In case of refusal, the supplier search algorithm goes back and makes a new attempt – it chooses another random node from the distributed hash-table and connects to it.

Theoretically, randomizing the supplier search increases the level of data storage security to some extent, as a possible attacker would not be able to guess which node will be the next supplier of the given user and accordingly would not be able to replace it with a node under their control.

The BitDust project does not maintain a vast hardware infrastructure, only some for testing purposes - every supplier in the network is a device owned by an independent person. So we do not even have a chance to keep track of your personal data.

