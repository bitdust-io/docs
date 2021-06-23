# Roadmap

In the section below you can find a more detailled description of the future roadmap.
You can find more in-depth information about certain features within other parts of the wiki.
PLEASE NOTE: THIS ROADMAP CAN CHANGE AT ANY TIME.

The section is split into two sections. First features we have already put on the roadmap.
Second there are features we are thinking about to put on the roadmap in the future. 
Please be aware that the timelines are an indication.


## Q2 2019 Stable Beta version

The BitDust contributors have already created an alpha version which makes it possible
to install the user's client on your local machine. This alpha version is already available
and can be installed for Windows, Linux and Mac. The basic features include the following:

* Create an account
* Upload/Download of data
* Share data with trusted friends/contacts
* Find friends and add them
* Encrypted chat with friends

We have come for already but we need to set-up a more stable version of the alpha release to 
make it into a Beta version. In addition we will make the UI more user friendly.


## Q3 2019 Implement Blockchain

In order to track the different states of the network we will be implementing an open source
python based blockchain. The miner will play a great role in validating the changes in the 
network. You can read more about the way we want to approach this in the section BitDust Blockchain.
In short the BitDust blockchain will:

* Provide users the ability to rent space with suppliers with the BitDust token.
* Suppliers will receive BitDust tokens for the service they provided in terms of storing user's data.
* Provide mining rewards in the form of BitDust tokens to miners for maintaining the BitDust blockchain.
* Provide the ReBuilder with a reward in BitDust tokens for rebuilding data and finding a new supplier.
* Provide the ability of a rating system for suppliers and pick out only the best ones for data storage.
* Provide suppliers with the ability to publish their rates and available space.


## Q3 2019 The ReBuilder

At this point in the BitDust software we implemented a mechanism for automatic data rebuilding,
to be able to reconstruct missing data segments when updating a lost supplier.
The whole process is fully automatic and does not require any actions from a user in order
to maintain downloaded data into the BitDust network.

Intially we wanted to run the ReBuilding process on a users machine. However we want
to transfer this functionality onto other nodes that will support this rebuilding process - 
we call the ReBuilders. You can read more details about it in the ReBuilder section.

An interesting feature of the proposed approach is that the ReBuilders do not have access
to user's data, since they always operate with encrypted data.
This allows you to safely authorize to rebuild your data to any nodes within the BitDust network 
and repeatedly increase storage reliability and speed up of uploading and downloading data.
The whole process of the remote automatic recovery will occur entirely without
the participation of the user. After uploading your data to the network,
you can shutdown your computer, or simply stop the BitDust software.

There are different aspects in making sure the ReBuilding can perform their tasks properly which are:

* The process of Rebuilding. This is currently in development.
* The moment when a ReBuilder should start or stop their work.
* The reward the ReBuilder receives in BitDust tokens for performed work.

## 2020 Create an Alpha for supporting roles within the BitDust ecosystem

Currently if you want to perform any of the supporting roles within the BitDust ecosystem you would 
need to do it from command line. Unfortunately we don't yet have an easy to use graphical interface
for supporting roles. We would like to create this so any one with basic computer knowledge can support
the BitDust network.

## 2020 Mobile BitDust application

We spend a tremendous time on our mobile phones. We use mobile phones for everything. All of the major
systems have a mobile integration. The BitDust contributors see going mobile as a huge untapped potential.
A device that is always online and only becomes faster and with more storage in the years to come. We want
to not only provide users with the possibility of accessing their files and chat via their mobile phone, but
also provide them with the opportunity to become a mini supplier. Providing storage back to users.

## Ongoing: Upgrading the graphical interface

We will continuously upgrade the user's graphical interface. Not only from a look and feel perspective,
but also from a feature perspective. We are currently thinking of potentially implementing the following
features in the future:

* Ability to create folders.
* Ability to share and alter data.
* Ability to chat offline.
* Ability to share offline.


#Distant possible features


## Chat/Video/Conferencing

We have already implemented a simple functionality to transfer encrypted private messages between nodes.
They are transmitted directly from sender to receiver, protected with digital signature of the sender
and encrypted with the secret key of recipient before sending it to the network.

In parallel with the development of the graphical user interface, we have developed a method
for the simple exchange of short messages just like in a typical chat system.
The history can be stored on a user's suppliers so it can be accessible at any time.

We are thinking of also introducing a streaming voice and video transmission
and implement a fully distributed and safe conferencing in the future.



## Decentralized Mail

It would be convenient to provide users with a familiar environment for the conduct of personal 
correspondence.
It is proposed to use a  mail SMTP / POP3 / IMAP client, which the user usual uses for 
transmitting/receiving e-mails.
This does not require a user to install anything else.

In the BitDust software we have already implemented a basic functionality for direct transfer 
of protected messages from one node to another.
Our plan is to use standard protocols SMTP, POP3 and IMAP to
create a universal interfaces between the user and other nodes within the BitDust network.

At the begining of the client software, we could create a couple local mail servers for input and 
output mails. These servers are pretty small and acts as a
intermediate script between the user's email client and the program BitDust.

After switching on that functionality in the BitDust software, 
the user will only need to configure a mail client that is most convenient for him/her.

At the moment there is not a final decision on the format of e-mailboxes
within the network BitDust. Probably they will be formed based on user's IDURL, for example example
http://p2p-id.ru/veselin.xml will be translated to veselin@p2p-id.ru.



## Anonymous logon

At the moment, user identification in the BitDust network let you hide your personal data 
and uses only short text identifiers.
There is no required to provide personal data like your email, phone number, etc.
BitDust contributors have no detailed information about the users of the software.

However, the user's IP address at this stage of the project development can not be hidden - it 
is published in his identiy file in a open or semi-open form.
We can talk about pseudo-anonymity in the BitDust network.

The implementation of the algorithm of hiding the real IP address of the user will provide:

+ anonymously store and distribute data across the network
+ a completely anonymous correspondence
+ create a personal sites whose owners are almost impossible to calculate


## Global search

We would like to add a search engine within the BitDust software.
This provides users with the ability to find a data in the global space which is granted a full read access - 
similar to torrents.
You will have the ability to add keywords which makes up the global search index. 

In a few simple steps the owner of any uploaded data can prepare the necessary information
and puts it into a global registry, which is stored into the distributed hash table.
Special "crawlers" sooner or later will visit the newly created topic,
validate it and make the appropriate changes in the global index.

This functionality will provide a completely safe and independent data distribution over 
the BitDust network, uncensored and possibility to exert any pressure on users by third parties.
This is a significant advantage in comparison with classical torrent trackers.

<div class=fbcomments markdown="1">
</div>