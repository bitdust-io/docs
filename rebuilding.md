# Automatic Rebuilding

In this section we describe the methods of automatic data rebuilding. Note, the process of automatic data rebuilding by the ReBuilder is still being worked on and will be released at a later time. However you can still read about the inner workings of the process of automatic data rebuilding below. In this section we cover the following items:

* [Data Redundancy](#data-redundancy)
* [RAID Transformation](#raid-transformation)
* [ECC codes](#ecc-codes)
* [Reassembly](#rebuilding)
* [Local Data Copies](#local-data-copies)
* [Supplier Change](#supplier-change)
* [Supplier Search](#suppliers-search)


## Data Redundancy 

In the section [Data Storage](storage) we described a mechanism of creating distributed user data copies in BitDust network. Within this article we describe a method of data partitioning into separate fragments, which enables dynamic recovery when data was lost and further redistribution of that data to more reliable nodes within the network.

Data uploaded to the users suppliers are stored with double redundancy and are organized into a RAID array for enabling the possibility of their recovery when data is lost.

The storage is organized in the following way: 

+ the first layer contains input data and is called "Data" 
+ the second layer has the same size but modified content and is called "Parity"


## RAID Transformation 

Different combinations of Parity fragments enable Data fragment recovery on the machine of a new supplier, who was recently replaced the previous supplier that went offline. Parity fragments of each block is created by conducting a XOR operation on each byte between several Data fragments of this block and is prepared for other suppliers. 

When one or more suppliers arer lost we still can restore the missing Data fragments from the fragments downloaded from other suppliers. When this initiated we need to do a XOR operation on each byte between the available Parity and the Data fragments once again.

The so-called iterative algorithm continues the work until it can restore at least one lost fragment in one cycle. For example, Data fragment recovery in one position on the first iteration allows restoring the Parity parts in other positions within the next cycle, and then Data fragments will be restored in third position etc.  


## ECC Codes

When building a RAID array so-called EEC codes are used – these are combinations of best positions of Data and Parity fragments in the suppliers are set. Here "position" defines which fragments must be kept by a given supplier.

For each of the possible combinations of suppliers the optimal EEC code was calculated – it defines the framework of mutual bracing of Data and Parity fragments in the layers and the maximum quantity of simultaneous errors, which may occur not leading to the block sustainability loss. Here you can see the allowable number of possible losses for each of the possible combinations of suppliers:


| **ecc code**              | **number of suppliers**       | **maximum errors**        |
|---:|:---:|:---:|
| ecc/64x64                 | 64                            | 10                        | 
| ecc/26x26                 | 26                            | 6                         |
| ecc/18x18                 | 18                            | 5                         |
| ecc/13x13                 | 13                            | 4                         |
| ecc/7x7                   | 7                             | 3                         |
| ecc/4x4                   | 4                             | 2                         |
| ecc2x2                    | 2                             | 1                         |


Thus percentage of possible losses is 50% for 2 suppliers and up to 15% for 64 suppliers. The greater the number of possible errors you can have, the more time you have to reassemble the lost fragments and the more stable the data storage is. In essence more suppliers should theoretically give you more a reliable storage space. But the greater number of suppliers you use, the more memory and network connections are required from your local operating system.


### ATTENTION!

    By exceeding the number of possible errors, you should expect complete
    loss of the uploaded data. The mechanism of automatic data recovery
    allows swiftly fixing encountered errors and enables
    new distribution of data on reliable suppliers’ nodes.

    The BitDust team is never responsible for suppliers that go offline and also never responsible when data is lost.



## Rebuilding

The algorithm of dynamic data recovery cyclically runs a sequence of actions aimed at constant maintenance of a state in which data can be downloaded from the network. The is the main responsibility of the supporting role of the ReBuilder (future feature).

In each algorithm iteration the BitDust software will make a decision about your suppliers based on the previously collected statistic data and current connection status. The least "reliable" supplier can be fired and another random node can be found in the BitDust network to replace them.

After changing the supplier, those fragments which were allocated on the old node are lost. Right away the ReBuilder should start the "rebuilding" process to reassembly of these fragments on a local computer and places them upon completion to the new node. Based on your ECC mode and number of suppliers a set of data fragments will be downloaded by the Rebuilder upfront from other suppliers which are available at the moment.

At each iteration of the recovery algorithm there is a reassembly of one single block of your data, software will be put it in a temporary folder on the disk of the ReBuilder to arrange the network delivery to a remote supplier node and removes those fragments afterwards.

To rebuild one lost fragment the ReBuilder needs to combine the Data and Parity fragments from reliable nodes and run the RAID process on that set. This takes some CPU time, because you doing huge amounts of XOR'ing in total - multiple times per each and every byte of your data. When being a ReBuilder it is important to have the right hardware capabable of performing the XOR'ing process.

The order of data assembly is organized by the time of the creation of each copy – it will first restore the most recently uploaded data and then sent it to reliable suppliers. BitDust keeps track of all running uploads and downloads and also "remembers" pending requests. 

The total time of the Rebuilding process depends on total size of your uploads, CPU frequency and network bandwidth limit.
Currently we have implemented a very basic scenario when only one active upload/download process is running and all jobs are organized in a queue.

Here is a short representation of the common sequence of actions at each iteration:


1. decision on supplier change was made – the least "reliable" node in the current supplier set is identified
2. global network lookup found a node which is ready to become a new supplier for the user
3. process of downloading already allocated data fragments from other suppliers is launched
4. for each block a RAID procedure for recovery of the lost fragments on the older node is done
5. restored fragments are uploaded to computer of the new supplier 
6. after successful upload the restored fragments are deleted from the local disk drive (optional)
7. rebuilding loop restarted from step 3. - next uploaded file will be taken from the queue to be recovered


## Supplier Change

The key pint in the mechanism of automatic data recovery is the method of making a decision about identifying and changing the bad supplier. After the decission is made the ReBuilder will start it's work to perform the rebuilding process for a user and place it at a new supplier (Note: this is a future feature that will be released).

Chosen EEC code influences the amount of possible mistakes in RAID array you can handle. In other words the amount of possible missed fragments in each block when you still can reassemble the whole block. 

At each iteration of the algorithm of automatic recovery the estimation of number of connected suppliers at that moment is done, as well as the matching of it to the possible number of losses for the given EEC method. If the number of inactive suppliers becomes critical, then the momentary change of one or several suppliers will be done automatically and the reassembly of all uploaded data and their transfer to the new nodes is underway. This is the main task of the ReBuilder.

At the moment those methods were implemented on a basic level and needs further development for optimal decision making. However this requires a real environment for testing and we need greater number of real users, which dynamically log on and out of the network to optimize the future solution. For now we are thinking about the best starting point and move from there.

In the future we plan to boost this functional so that it could "predict" beforehand who will go offline and needs to be replaced by previously collected daily/weekly statistics. 

In the future we plan to create conditions for external praising of suppliers who provide reliable data storage. This future feature will have to worked out and off course the roadmap is open for change.


## Suppliers Search

Supplier change and the search of a new node in the BitDust network is done under these present parameters:

+ the volume of requested from the network space
+ the number of suppliers in the combination – it depends on the chosen EEC method

For this the distributed hash-table is addressed and the random node is chosen. Then this node is connected and sent a request to provide a service of storing data for the user. By acceptance the chosen node becomes a new supplier for that user. In case of refusal the algorithm of supplier search goes backwards and does a new attempt – chooses a random node from the distributed hash-table and starts connection.

Theoretically randomization of suppliers search method allows the increase of the level of data storage security to some extent as a possible attacker would not guess which node will be the next supplier of the given user and accordingly would not be able to change it with the node under his control.

The BitDust project does not maintain a vast hardware infrastructure, only done for testing purposes - every supplier in the network is a device owned by an independent person. So we do not have even a chance to keep track of your personal data.


<div class=fbcomments markdown="1">
</div>
