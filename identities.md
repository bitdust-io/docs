# User Indentification

In this section you can mainly read about user identification and how it is done within the BitDust network. 


* [Identity files](#identity-files)
* [ID-servers](#id-servers)
* [IDURL address](#idurl-address)
* [Hosts rotation](#hosts-rotation)
* [Global unique entity ID](#global-unique-entity-id)
* [Digital-signature](#digital-signature)
* [Private key](#private-key)
* [Your privacy](#your-privacy)


## Identity files

For other nodes to connect to a user's machine they have to know the address of the user's computer in the Internet. These contacts are stored in an XML file, which is called __Identity__. By connecting to other nodes the download of the identity files takes place and the received information is used for direct transfer of service packets. 

In the user identity file the following information is stored:

* contact data of network protocols for connection with his machine 
* open part of user's personal key 
* digital-signature for protection from modifications of file content
* a list of IDURL addresses in the Internet by which the file is available
* date of file creation
* version of BitDust software run on users computer

To log on to the BitDust network each user needs to create a personal identity file – this happens automatically when you create an account within the BitDust program the first time it starts.



## ID-servers

In theory the location of a user's identity file can be anywhere, however it is important that it is easily accessible for all other nodes in the network. For example, a user can put the given file on his personal website. By doing so he/she needs to assure the possibility to easily update the given copy from the original, which is stored on the machine of the user. To guarantee a more secure and fault tolerant interaction between nodes in the network you can store multiple copies of your identity in several places. 

This kind of storage is done with the use of multiple machines also called ID-servers or Identity servers, whereby copies of all identity files are stored. These servers are maintained by BitDust community (but also ID-server can be started on any other machine) and are all listed in the publicly available [default_network.json](https://github.com/bitdust-io/public/blob/master/default_network.json) file.

An ID-server is a part of BitDust program, but by default it is turned off in the program settings. If required each user can turn on this option and start such a server on their own computer – afterwards the ID-server will be automatically start when starting the BitDust program. An ID-server consume almost no computer resources, but will allow you to support other nodes and increase the overall fault-tolerance of the entire BitDust network.

If you feel enthusiastic now, then you can read more about how to become an identity server within BitDust network. See the [Start new Identity Server](identity_server.md) page or how to run a [Full Seed node](seed_node.md) from scratch.

If you plan to maintain your BitDust node for a while and support the network it make sense to include your node into a list of "well known" nodes, which are hard-coded in the [default_network.json](https://github.com/bitdust-io/public/blob/master/default_network.json) file.

You can also Fork the [Public Git Repository](https://github.com/bitdust-io/public), modify `default_network.json` file in your forked repository and start a [Pull Request](https://github.com/bitdust-io/public/pulls) with your changes - this way we can collaborate all together and maintain a list of the most reliable BitDust Identity servers.

Contact the BitDust contributors to notify about startin a new Identity Server and one of the developers will approve your Pull Request.



## IDURL address

Each BitDust user is identified by IDURL key – this is an address of the identity file in the global Internet network. This identifier is related to the device running the BitDust software, but not to person who is managing this device. Only by using yhe Private Key stored on that device you can change your identity in the network.


Example IDURL might look like this:

        http://first-machine.com/alice.xml

 
And the identity file itself has the following aspects:

        <identity>
        <contacts>
          <contact>tcp://123.45.67.89:7771</contact>
          <contact>udp://alice@first-machine.com</contact>
        </contacts>
        <sources>
          <source>http://first-machine.com/alice.xml</source>
          <source>http://server-two.net/alice.xml</source>
        </sources>
        <certificates/>
        <scrubbers/>
        <postage>1</postage>
        <date>Sat Dec 13 14:08:36 2014</date>
        <version>
          sources Linux-3.11.0-15-generic-i686-with-Ubuntu-12.04-precise
        </version>
        <publickey>
          ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgGcYwhNipj6yJyEaD77qLNrJ ...
        </publickey>
        <signature>
          1557824826897671730886854628410961132377100189021332866347553795 ...
        </signature>
        </identity>


Each identity file can have several copies, stored on different servers – for ensuring fault-tolerance of a users identification within the BitDust network. Thus each node can have several IDURL addresses, making it possible to identify it.

A user has the ability to create an authentic identifier within the BitDust network – for example, starting an ID-server for hosting of their site and allocating their personal identity file. For instance: 

        http://veselin-penev.com/id.xml


It is preferably that machines running ID-servers have correctly adjusted the domain names. Then the IDURL identifiers of the users, whose identity files are stored there, will look more attractive.
    
But off course it is not mandatory to buy a domain name to run your own ID-server. In that case ID files on your host may look like this:
   
        http://123.45.67.89/id.xml

    
For some reasons this can be more preferable, in case you do not wish to depend on global DNS providers.

The system is designed in such a way that even in the case of failure of one or more servers that store your Identity file, other users can download it from other ID-servers and are able to connect with you. The program continuously monitors your ID-servers and in case of failure triggers automatic distribution of your Identity file on another available ID-servers, and notifies your active nodes immediately.



## Hosts rotation

Periodically the software will trigger a method to check and propagate your identity file to other nodes. Before it starts it can switch your current "primary" ID-server to another one - another ID server will be found and your identity file will be sent to that host. Your main global IDURL address will be changed because a new server will be placed on the first position under a `<sources>` tag, for example:

        <identity>
        <contacts>
          <contact>tcp://123.45.67.89:7771</contact>
          <contact>udp://alice@host3.org</contact>
        </contacts>
        <sources>
          <source>http://host3.org/alice.xml</source>
          <source>http://first-machine.com/alice.xml</source>
          <source>http://server-two.net/alice.xml</source>
        </sources>
        <certificates/>
        <scrubbers/>
        <postage>1</postage>
        <date>Sat Dec 13 14:08:36 2014</date>
        <version>
          sources Linux-3.11.0-15-generic-i686-with-Ubuntu-12.04-precise
        </version>
        <publickey>
          ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCgGcYwhNipj6yJyEaD77qLNrJ ...
        </publickey>
        <signature>
          1557824826897671730886854628410961132377100189021332866347553795 ...
        </signature>
        </identity>


Final IDURL will be updated like so:

      http://host3.org/alice.xml


Both IDURLs are pointing to same device now, but we only switch the main location of your identiy file - to be used by all other nodes who are talking to you. To do that the software will "propagate" your new identity file to all of your currently active contacts. Also it will update copies on ID-servers you are using already: "first-machine.com" and "server-two.net".

The software will try to keep you "nickname" unchanged, for example if "host3.org" server already stores another "alice.xml" file signed with another public key it can not be used by you, because this name is already taken. A username is the name you pick in the beginning and can never be changed. At first the nickname is based on your username, however a nickname can be changed at any time.

We expect the regular BitDust user to be able to spawn an own ID-server easily - a lot of "hosters" in the network are required to be able to operate in the network in reliable, private and in a safe way.

BitDust software that is running on your machine will automatically "migrate" or "anonymous" your identity in the network and so it will be almost imposible to "block" or "attack" your presence in the network.



## Global unique entity ID

BitDust supports a global unique ID for any existing object (file, group, user, etc.).
This is an example of a full remote path to file "cat.png" within the BitDust network:

        group_abc$alice@first-machine.com:animals/cat.png#F20160313043757PM


A full identifier consists out of several parts, for instance:

* identity server host (DNS name or IP:PORT address): first-machine.com
* user identity filename (without ".xml"): alice
* key ID: group_abc
* backup ID: animals/cat.png
* version name: F20160313043757PM


If an identity server was set using IP:PORT format the global ID might looks like this:

        key_xyz$bob@123.45.67.89_8000:cars/citroen.png#F20160313052124PM


This approach has something similar with "remotes" and "branches" in Git. For example a full remote file path in Git can be written down like so:

        https://github.com/vesellov/bitdust.devel/blob/master/automats/automat.py


Looking more deeply we can split this URL by several parts:

* server host: github.com
* user account ID: vesellov
* repository ID: bitdust.devel
* branch ID: master
* file path: automats/automat.py



## Digital signature

By creating or adjusting a user's identity the generation of digital-signature takes place – it is connected to the file content and serves for the protection from all not intended modifications from third parties. Digital-signature is calculated from the file content via a Hash-function and for it's creation you need a Private Key, which is stored only on your machine.

The general principle of security of a user identity from adjustment is based on the fact that all other nodes necessarily check the digital-signature and file content accordance each time they get a new copy from its identity – this is a standard method in cryptography called `VerifySignature`.

This framework helps to safely store and distribute a user identity files through any sources, which include also ID-servers. Machine owner, who started an ID-server, do not have any possibility to substitute content of stored there files. But they can easily delete them or turn off the server – for loss prevention of the identity file of each user it is stored on several servers all over the world. 



## Private Key

Upon first install of the BitDust program the private key is generated, this key protects the identity file and your personal data. Only this key can grant you access to the personal user's data and/or make adjustments to the identity file.

Within BitDust you cannot find any common schemes or methods of a user's authorization:
 
* not using a password
* not via email address
* no account recovery through answering a secret question
* not calling a support team
* no centralized storages of member accounts


#### ATTENTION!!!
    In case of losing your private key the user completely loses access to all their uploaded files. 
    It is highly recommended to make two or three copies of your private key on reliable and 
    compact media just after the program set up and hide them in a secure place.

The user responsible for the security of their private key. A private key should NEVER leave your computer on which it was generated – this potentially has a major impact on the security of your data.

We recommend using a modern anti-virus software or any other tools to arrange an extra defence from network attacks and other methods of increasing security level of your personal device. In addition to this, we advise you to look through useful information resources on this topic in order to raise your awareness. 



## Your privacy

Your identity file is distributed publicly on the network and at the same time is a unique source that allows other users to connect to your device.
The file does not store your personal data (name, surname, address, etc.) but contains technical and service information (nickname, IP address, RSA public key) required for BitDust to operate.

BitDust network protocol may be considered as [pseudonymous peer-to-peer](https://en.wikipedia.org/wiki/Anonymous_P2P) communication system.

While registering a new identity you will chose a "nickname" that will never change thru the life-time of that identity.
Your nickname may represent your real name or be a random string. It can be name of an animal or a president or anything else you wish other users to see when communicating with you via BitDust.

Also your identity file stores a networking information about your device such as IP address and TCP/UDP port number - that information identifies your "physical" location.

There are few possibilities in BitDust to reduce disclosure of your networking info and so "hide" your physical location from other users:

* Run your own ID-server on external device (which physical location may be disclosed - acts as a "shield") and re-configure your "master" device using [known-servers](https://bitdust.io/wiki/settings.html#known-servers-(string)) and [preferred-servers](https://bitdust.io/wiki/settings.html#preferred-servers-(string)) settings before registering new identity in the network
* Enable proxy-transport network service that will re-route all your encrypted BitDust traffic via another randomly selected node - this way you can almost completely hide your real IP address from others
* Run your own proxy-router on external device (which physical location may be disclosed - acts as a "shield") and re-configure your "master" device using [preferred-routers](https://bitdust.io/wiki/settings.html#preferred-routers-(text)) setting
* You can use VPN services to enable lower level networking protection on your device and BitDust will work on top of that via same TCP/UDP protocols - other users will recognize IP addresses of the VPN providers, but not your own in that situation

In other words, it is impossible to provide 100% guarantee of complete concealment of your physical location in the network and in general true anonymity is not the main goal of the project - but can be boosted to a very high level using additional techniques.



<div class=fbcomments markdown="1">
</div>
