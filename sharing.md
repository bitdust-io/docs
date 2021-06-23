# File sharing

We are not isolated as human beings and we recognize that users have the desire to share their data with trusted contacts. In this section we explain how data is shared safely and securely through the following items:

* [Master Key](#master-key)
* [Shared keys](#shared-keys)
* [Grant access](#grant-access)
* [Audit access](#audit-access)
* [Receiving shared keys](#receiving-shared-keys)
* [Reading shared data](#reading-shared-data)


## Master Key

Since every piece of your personal data in the BitDust network is stored on the machines of other users, it is important to know that all data is always encrypted before it leaves your computer - the method of protection is described in detail in the article [Data Security](security.md). Your main private key, here and below, we will refer to it as a "Master Key" is used to encrypt and decrypt your personal data for storing on the suppliers machines.

For your personal safety, you should make a backup copy of the Master Key and put it in a safe place immediately after installing BitDust on your device. In any other cases, the Master Key should never leave your device and under no circumstances should it be transferred to anyone else. Only the Master Key protects your personal data and provides access to the BitDust network.


## Shared keys

In addition to the Master key, there are other private keys within BitDust that you can use to manage your data. The BitDust software implements an extra logic to use the same cryptographic methodds. However the software makes it possible to work with many different keys.

Using additional private and public keys in BitDust is very similar to what happens in the real world, for instance you have multiple keys on your keychain to open and close different doors. For example if you have a good friend visiting your place and you would like to provide him shelter in one of your guestbedrooms after a night of heavy drinking:), you will probably give him a copy of the key you have on your keychain to be ably to unlock this room. But you will still have the original key for yourself. Thus, both you and him will have access the guest bedroom. However there might be rooms within your house that you want to keep locked and that it only be opened by you. 

Within BitDust you can at any time create a new additional private key for sharing purposes and use it to encrypt some data that will be uploaded to your suppliers's machines. The data is stored in a distributed way, in the same way when you encrypt data with your Master Key - this is described in detail in the article [Data Storage](storage.md). You will have the possibility to switch from your Master Key to an additional key when you want to share a file.

Later on you can transfer this additional key to another user who you trust and this user will have the ability to download this particular piece of data and decrypt it on his own device. Thus, we can exchange personal data with each other.

When you want to create additional keys you can perform the following actions:


* create a new key by giving it a name and store it locally
* create a new key with a randomly generated name
* delete an existing private key
* backup and store the keys on your suppliers - will be encrypted with your Master Key
* send the public part of a given key to another "un-trusted" user
* send the private part of a given key to another "trusted" user
* view a list of all keys: created by you or received from other users
* perform an "audit" process of a given public key and verify that another user also posses the exact same copy of that public key
* perform an "audit" of given private key and verify that another user also posses exactly same copy of that private key
* use a private key to encrypt data downloaded to the BitDust network
* use a private key to decrypt data downloaded from the network


You will find your additional private keys in the `.bitdust/keys` folder,
currently BitDust software is using the [RSA algorithm](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) which a widely used encryption method.
Those methods were implemented using [PyCrypto](https://pypi.org/project/pycrypto/) library.

Note that most of the actions performed are automatically. We just want to describe the steps BitDust performs to provide you with more insight into the inner-workings of the software.


## Grant access

When transferring an additional key from one user to another, one of the text files from the `.bitdust/keys` folder is actually sent to the remote recipient's machine. The key is not transmitted in plaintext but it is encrypted using the public part of Master Key of the recipient before sending - only the "trusted" user will be able to decrypt this text file and get a copy of the transmitted additional key. The BitDust program on his machine will receive the key and save it in the new text file in the `.bitdust/keys` folder. When you share a additional key with another user you are basically providing that user access to all your data that is encrypted with that particular key. The recipient will automatically see which files you shared within the BitDust program (section "shared files").

It is important to understand that this action is "irreversible"! You can not "take" the key back after you handed it to the recipient. In fact, after you have passed the key to another user - both of you are almost completely are "fully equal" owners of the data that was encrypted with that additional key.

We say "almost equal" ownership when you share data, the data is still stored on your suppliers, but not on the suppliers of user your shared the data with. So you have always "more rights" inside your own distributed storage than anyone else. For example, at any time you can request to your suppliers to delete the files you shared with other users. But be aware that a user who you shared data with could always have downloaded the file before you request to delete that data from your suppliers. 



## Audit access

The most important role of the supplier is to store and provide access to files. To achieve this, each supplier must have specific instructions and a well-defined order of actions that they must perform at the time of the request to the distributed "shared" data on his device from you or a "trusted" user. Since all data that the suppliers store is encrypted, even if suppliers would send your fragments of your data to third parties you can still remain calm - only those who posses the right key will be able to "read" your files.

However, the BitDust software implements methods for filtering and validation to "access requests" for all data that is uploaded to the network. By default the supplier will "check" that the one who requests a particular piece of data has the correct additional key to decrypt the data. The supplier must "audit" the user's key, which refers to it the data in question. To do this, the supplier must keep the public part of the key, which was used to encrypt the data. This public key is usually received from the user, exactly at the moment when you grant access to the data to the "trusted" user.

To keep it short, below is the general plan implemented in the BitDust software which executes on your device when you transfer one of your additional keys to another user:


1. checking the connection status of the trusted user's computer
2. audit of the master key of the trusted user
3. sending the public part of the additional key to all your suppliers
4. forwarding the private part of the additional key to a trusted user
5. forwarding a list of file names that have already been encrypted with this additional key to a trusted user



## Receiving shared keys

In the previous paragraphs, we described methods for transferring access rights of your data to another user who you trust. Next, you will find detailed information about what happens on the device of the trusted contact and how they can use the additional key they received from you, the user, to download the "shared" data.

An assumption is made that the BitDust program is running on both devices and is connected to other nodes within the BitDust network at the time when an additional key was started. In case when the "donor" or "recipient" were not connected to the network and did not have the opportunity to directly exchange service packages via the BitDust "channels", the process will fail and no access will be granted at all. In short to share data both parties must be online to share data. We are currently looking into the ability to re-use existing keys for sharing purposes. This enables offline sharing when you already shared at least one key with each other.

BitDust on the machine of the "trusted" user is constantly in a waiting state to receive incoming service data packets and is always ready to accept a new incoming access keys. After receiving and decrypting the file with their own Master Key, it will be stored in the `.bitdust/keys` folder. You can always find out the full list of all access keys that have been passed to you from other users - it's important to note that each key has a unique global identifier that looks like this:

        share_0780f0d64b017303a0d81865eee009f1$veselin_penev@some-id-hostname.net


The initial part of the identifier before the character `$` is called "key alias" and serves to identify a particular key among a set of additional keys created by this user. The second part after the `$` character is the unique global identifier of the user who first generated the key. For more details about the identification of users in the BitDust network, you can read in the article [User Identification](identities.md).

This method of identifying access keys always uniquely defines who is the creator of the data and on whose suppliers the encrypted fragments of files in the BitDust network are actually stored. In other words, having received a new access key from someone, by default you will always know where the "shared" files is located.



## Reading shared data

So to access the "foreign" files, you need to use the key identifier to determine the "location" of the data. We use the word "location" in a figurative sense, since all data is stored completely distributed on the suppliers' machines. For downloading fragments of files and decrypting them, it is necessary to determine the current active suppliers, connect to them and request all the fragments of data related to that given "common" file.

In BitDust, the list of your suppliers is stored and maintained not only on your own device, but also in a distributed hash table - your suppliers automatically support and periodically update these "globally distributed" records. Thanks to this, any user always has the ability to "scan" the list of your suppliers and find out where they need to go to download those files to which you "granted access." The process of "scanning" that list takes some time, depending on the number of suppliers you have. In more detail, you can see how BitDust uses these service records in the article [Distributed Hash-table](dht.md).

After connecting with the "foreign" suppliers, you can request the necessary pieces of data related to a particular "shared" file. If the access key you received from the "donor" is valid, "external" suppliers will accept your request and the BitDust software on your device will receive the needed fragments, decrypt, combine into one chunk and create the exact same copy of the "shared" file of which "donor" granted you access.



## Customer data flow step-by-step

Let's try to describe everything that happens with your data step by step at the moment of transferring access to another user.

* The BitDust program is already running on your device
* And you already generatged a private key and a new identity for yourself in the network - 
* In the application you will click a button "Create a new Share" and the software will create a new virtual location in your files catalog called a "share"
* A new private key will be generated automatically and you will be able to verify the key in the app
* Via "Share Key" button in the app it is possible to transfer a key to another device/person - supposed to be done with most secure way as possible
* Your trusted person also is runnig BitDust and also have an identity in the network
* As he receives your private key he keeps it in his own files catalog as well and able to see the files listed in this "share"
* Both of you could upload & downlad files into that "shared" location easily via the app
* Each uploaded data fragment is stored on your own suppliers - on the suppliers hired by creator of the "share"
* Also all suppliers will keep in touch with you and another user as well - be able to notify you both about any updates on the "share"

The software suppose to handle all of the communications and transfers automatically as well as storing the data reliable and secure as possible.

This whole process is happeing in the application peer to peer between devices running BitDust software and connected to the Internet.

The engine is sending and receiving signed and encrypted data packets via BitDust network and the app is enabling user interface for specific platform.




<div class=fbcomments markdown="1">
</div
