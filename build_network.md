# Your own BitDust Network from scratch

In this section, you will learn how to create and maintain your own fully isolated and private BitDust network under your complete control.

It is also very easy to setup completely public network which is fully open for everyone to join and communicate all together.

Here we assume that you have basic Linux systems and system administration skills. You don’t have to be a Python expert to manage BitDust, but you need to know how to use SSH, how the Debian system works and what "WEB server" actually means.



## Infrastructure requirements

You will need several computers connected to the Internet, these can be:

* dedicated or virtual servers
* cloud servers
* home or office computers - make sure port forwarding is configured in that case

It is also recommended that you already have the domain names assigned to your hosts, so that you can use the DNS names for your hosts instead of the public IP addresses.

In order to show the whole process of creating a BitDust network from scratch, we will use an example of few computers that will be the core of our new network. All other nodes can join later in any number as soon as the BitDust kernel network is configured.

Suppose you already have 4 Debian Linux servers under your control with SSH access and these domain names:

* host-a.com
* host-b.com
* host-c.com
* host-d.com



## Part 1: install BitDust software

One by one connect to each machine via SSH and perform following steps to install BitDust software.

First install all dependencies with APT package manager:

    sudo apt-get update
    sudo apt-get install git gcc python3-dev python3-virtualenv python3-pip


Then using GIT you need to clone the Public BitDust repository directly from GitHub:

    git clone https://github.com/bitdust-io/public.git bitdust


Now you will create a virtual environment with all the required Python dependencies inside it, making sure BitDust software will run fully isolated.

Single command should make it for you automatically, all required files will be generated in the `~/.bitdust/venv/` folder:

    cd bitdust
    python3 bitdust.py install


Last step to make BitDust software ready to be used is to make a short alias in your OS:

    sudo ln -s -f /home/<user>/.bitdust/bitdust /usr/local/bin/bitdust



## Part 2: start DHT network

### Brief info about Distributed hash-table

[Distributed hash-table](https://en.wikipedia.org/wiki/Distributed_hash_table),
or `DHT`, provides an interface close to associative array or dictionary with key/value pair where storage of all pairs (key, value) is distributed into multiple nodes.

The nodes in the DHT network are organized in the form of an abstract tree. The node must know at least one of the "ancestors" in order to connect to the network for the first time. The nodes that connect later use those nodes that are already running and find their place in the abstract tree according to a [Merkle Tree](https://en.wikipedia.org/wiki/Merkle_tree) algorithm. Moreover, if some of the nodes fail, the entire structure remains stable and the lost data is duplicated to other nodes automatically.

The BitDust software implements a DHT network which is tightly integrated with other components. The implementation was adopted from [Entangled project](http://entangled.sourceforge.net/) which uses UDP protocol as a transport layer.

To get more information about how BitDust uses Distributed hash-table go to [BitDust DHT](dht.md) page.


### Genesis seed node

Therefore, the first step to launch the BitDust Distributed hash-table network is to launch the root node of the tree or the "genesis" node, as we call it. We need to choose one of 4 nodes from our core network and reserve it for such purpose.

Let's use `host-a.com` machine to run the "genesis" DHT node:

    ssh host-a.com


BitDust software consists of many different components that are managed by "network services" organized within the software. By default, all services are configured to best serve the end user of BitDust - the consumer. But since we do not need to run this "role" on our "core" servers (they are intended for servicing and providing resources to end users), we must disable some of the network services for the BitDust software to work correctly:

    bitdust set services/customer/enabled false
    bitdust set services/supplier/enabled false
    bitdust set services/proxy-transport/enabled false
    bitdust set services/proxy-server/enabled false
    bitdust set services/private-messages/enabled false
    bitdust set services/nodes-lookup/enabled false


If you run BitDust software on your home or office computer behind a NAT router, and you do not have a public IP address and a direct Internet connection, you will have to configure port forwarding yourself. This is necessary for all "core" servers because they must be able to receive incoming connections from other nodes in the network. So please make sure UDP port `14441` is open.

Now we will prepare configuration for DHT node itself. First set which UDP port you are going to use to receive incoming packets within DHT network:

    bitdust set services/entangled-dht/udp-port "14441"


Tell BitDust to use that node as "genesis" DHT seed:

    bitdust set services/entangled-dht/known-nodes "genesis"


Now just start BitDust as a "daemon" process - it will run in background and operate as a DHT "genesis" node on `host-a.com` machine:

    bitdust daemon


You can verify current status of your DHT node by calling to BitDust REST API interface from command line with `curl` tool:

    curl localhost:8180/network/status/v1?dht=1


The output from `curl` should give you `"contacts": 0` which means there is no other nodes connected to `host-a.com` yet.


### Connect seed nodes to each other

You have a DHT network of 1 single node now, not much at all actually.

Let's connect the other 3 nodes to the first one. The first steps are similar to what we have already done with the "genesis" node:

    ssh host-b.com
    bitdust set services/customer/enabled false
    bitdust set services/supplier/enabled false
    bitdust set services/proxy-transport/enabled false
    bitdust set services/proxy-server/enabled false
    bitdust set services/private-messages/enabled false
    bitdust set services/nodes-lookup/enabled false
    bitdust set services/entangled-dht/udp-port "14441"


Now point the second node to the "genesis" node so that it knows where it should connect for the first time when entering the DHT network:

    bitdust set services/entangled-dht/known-nodes "host-a.com:14441"


Start BitDust on the second node:

    bitdust daemon


Verify connection status again with `curl localhost:8180/network/status/v1?dht=1` call - you should see `"contacts": 1` in the response on both machines: `host-a.com` and `host-b.com`.

Repeat above actions on `host-c.com` and `host-d.com` to connect all 4 seed nodes all together.



## Part 3: start Identity servers

### Brief info about BitDust authentication

Another key component of the BitDust network is Identity server.

Each active BitDust user, no matter he is consumer or provider of the resources, must have an "identity" within the network to be able to communicate with other nodes and be a part of BitDust community.

Your "identity" is a small digitally-signed XML file that is distributed across several Identity servers on the BitDust network. Such XML file contains important information about the device that describes how to connect to the user securely: IP address and port number, public key, username, etc.

When you contact another user in the network for the first time you both share copies of your identites and recognize how to connect to each other via Internet. BitDust software does all stuff automatically for you and establishes a secure private peer-to-peer connection between devices.

Therefore, other computers must have the latest copy of your identity in order to be able to communicate with you. For example, when your IP address changes, the new XML file will be automatically generated and "propagated" to the network.

This is the main purpose of the Identity server on the BitDust network - it stores the latest copy of your identity file. A remote user can always access one of the Identity servers, download the XML file, and be able to communicate with you.

Identity server uses HTTP protocol to serve XML files which it stores locally. To receive incoming identity files from other nodes it uses TCP protocol. Basically this is a very simple web server which works that way:

+ receives incoming TCP data from any remote host
+ validates input data - it must be a valid identity file
+ stores the file locally
+ periodically checks all of the stored files and removes identities which was not "touched" for a long time

To get more information about BitDust identities go to [BitDust User Indentification](identities.md) page.


### Install HTTP Web server

We advise you to use Apache2, Nginx or another Web server to handle incoming HTTP traffic and then pass it further to the Identity server process running on same host.

BitDust software suppose to be always executed without root permissions. Because of that you can not use port 80 directly in BitDust and easy way to do that is to redirect traffic via another "classical" Web server like Apache2 or Nginx.

Let's start with `host-a.com` machine and install first Identity server here. Make sure you set a hostname on your machine if you did not do it before and install Apache2 as an example:

    ssh host-a.com
    sudo hostname -b host-a.com
    sudo apt-get install apache2


Edit Apache2 main config file:
    
    sudo nano /etc/apache2/apache2.conf 


You need to add a line to set your domain name:
    
    ServerName host-a.com


Create a new `.conf` file for Apache2:

    sudo nano /etc/apache2/conf-available/host_a_com.conf


Use that sample to create Apache2 config, basically you can just copy & paste and only change domain name here:

    <VirtualHost *:80>
        ServerName host-a.com
        ServerAlias www.host-a.com
        ProxyPreserveHost on
        ProxyRequests Off
        RewriteEngine on
        ProxyPass / http://localhost:8084/
        ProxyPassReverse / http://localhost:8084/
        Redirect / http://localhost:8084/
        RewriteRule ^/(.*) http://localhost:8084/$1 [P,L]
    </VirtualHost>


Enable this configuration in apache2, run command:

    sudo a2enconf host_a_com


Configure proxy_http and rewrite modes in apache2, run commands:

    sudo a2enmod proxy_http 
    sudo a2enmod rewrite


Now restart apache2 server:

    sudo service apache2 restart


### Configure BitDust Identity server

Now configure BitDust on `host-a.com` node and set domain name for this new identity server, run commands:

    bitdust set services/identity-server/enabled true
    bitdust set services/identity-server/web-port 8084
    bitdust set services/identity-server/tcp-port 6661
    bitdust set services/identity-server/host host-a.com


If you run BitDust software on your home or office computer behind a NAT router, and you do not have a public IP address and a direct Internet connection, you will have to configure port forwarding yourself. This is necessary for all "core" servers because they must be able to receive incoming connections from other nodes in the network. So please make sure TCP ports `6661` and `80` are open.

Also you should let BitDust software know the whole list of all Identity servers inside the network:

    bitdust set services/identity-propagate/known-servers host-a.com:80:6661,host-b.com:8080:6661,host-c.com:8080:6661,host-d.com:8080:6661


Now restart BitDust to apply your configuration:

    bitdust restart


Now open your favority WEB browser and navigate to `http://host-a.com`. You should see an empty page with title "Identities on host-a.com".

To make life easier you can also configure your system to start BitDust software automatically when it reboots. For example on Debian system you can use `crontab` tool for that:

    crontab -e
    @reboot /usr/local/bin/bitdust daemon


Repeat same configuration on other machines in the "core" network. In that example we will have 4 Identity servers in total:

* www.host-a.com
* www.host-b.com
* www.host-c.com
* www.host-d.com



## Part 4: create first identities

Now it is time to finally create first "users" inside our small network which is actually almost ready to be used.

Let's create a fist identity on `host-a.com` machine:

    ssh host-a.com
    curl -X POST -d '{"username": "alice"}' localhost:8180/identity/create/v1
    bitdust restart


Congratulations! You just created your first BitDust user. Let's verify `alice` is online, if you run that `curl` request again it suppose to give you much more information than before:

    curl localhost:8180/network/status/v1?dht=1


Also we strongly advise you to always create a backup copy of your identity! Only from that backup file you will be able to restore it in case of lose. Your Private Key will be copied in the text file and you need to save that file in very safe place:

    curl -X POST -d '{"destination_path": "/home/<user>/bitdust_identity_backup_key.txt"}' localhost:8180/identity/backup/v1


Now continue and create other identities `bob`, `carl` and `dave` on the other machines. And do not forget to create a backup copies of the identities!



## Part 5: start traffic routers

### The purpose of the Proxy servers

As you should have understood from the previous sections, there are different types of nodes within the BitDust network — in other words, "roles". As conceived, the central role in the [BitDust eco-system](ecosytem.md) is the end user, the "customer". Other "roles" are designed to support the customer in one way or another and provide the customer with the necessary resources and services.

The preferred way to connect end users within the BitDust network is always using direct peer-to-peer connections - this is the most private, safest and fastest way to transfer data. However, in some cases, depending on the type of Internet connection and network configuration, a direct connection between two end users is not physically possible.

A possible solution to this problem is to use one or more intermediate nodes, which have a more open network configuration, to redirect traffic between two users located behind the NAT. 

For this purpose, the role of the "router" was created, which was implemented as a network service called "proxy-server". Any user by his own free will can enable and configure "proxy-server" service inside the BitDust software and help other users connect to each other.

Thus, the router will use the bandwidth of its Internet connection not only for its own needs, but also to help those end users who are currently using it. In other words, he will donate part of his Internet traffic to BitDust users.

At the same time, the Proxy server cannot read or modify the data that the end user receives or passes through it - the data is encrypted with keys that it does not possess.


### Configure BitDust Proxy servers

The "proxy-server" service uses TCP protocol to transfer data from/to the end user. If you run BitDust software on your home or office computer behind a NAT router, and you do not have a public IP address and a direct Internet connection, you will have to configure port forwarding yourself. Please make sure TCP port `7771` is open.

Let's start the "router" service on each node inside the "core" network.

To enable the Proxy server first you need to disable "proxy-transport" service - this is actually other side of BitDust proxy routing. Proxy Transport is a service which end user uses to connect to a random Proxy server within the BitDust network. Proxy Transport and Proxy srver must never run together on the same node and by default in BitDust software everything is configured to serve the best for the end user. That is why by default "routing" is enabled, but "proxy-server" service is disabled. Let's changed that:

    ssh host-a.com
    bitdust set services/proxy-transport/enabled false
    bitdust set services/proxy-server/enabled true


You can verify that configuration was successfully applied by checking the output from `bitdust states` command:

    bitdust states | grep proxy


The output suppose to be like that:

    6: service_proxy_server(ON) 
    11: service_proxy_transport(OFF) 
    50: proxy_router(LISTEN) 


It should be noted that it is not necessary to start the router service on machines that form the core of the network. We assume that the "routers" in the network will be numerous and their number will grow with the growth of the entire network - depending on the needs of users.

The core of the network, by design, should be stable and consist of only a few machines. By design, user data should not pass through these "key machines" - they play their main role only when the new user is initially connected.

We provide here detailed information on configuring services and roles in a simple network consisting of only four machines. In networks of many large sizes, it will be more profitable for you to run separate machines for each role and optimize overall performance.



## Part 6: start suppliers

The most valuable feature that BitDust provides you with is the fully independent and private distributed online storage. A "customer" is someone who consumes space from the BitDust network. And the "supplier" is the one that provides this space.

To get more information about BitDust storage algorithm go to [BitDust Distributed Storage](stprage.md) page.

As we already stated in a previous part - it is not necessary required to start multiple roles on the same node because of performance reasons. Here we have a very simple example of a network and we only have an intention to show how to use BitDust software and run a fresh network from scratch.

If we a talking about global public network, "supplier" role as well as "proxy server" role, suppose to be driven by many individuals all around the Wrold. Identity servers and DHT seed nodes suppose to be maintained by a smaller community of skilled developers.

So, let's assume that `alice`, `bob`, `carl` and `dave` are not part of the "core" network we just built, but simply enthusiasts who have just installed the software on their virtual servers and want to donate part of their drives to other users.

To become a supplier within BitDust network you just need to enable and configure "supplier" service:

    ssh host-a.com
    bitdust set services/supplier/enabled true
    bitdust set services/supplier/donated-space 50 GB


You can at any time check the current consumption of your donated storage with such `curl` request:

    curl localhost:8180/space/donated/v1


Now `alice` is ready to store data for other users. In the last part you will learn how to actually start using your own BitDust network.



### Part 7: start customers

### Prepare network.json file

...





<div class=fbcomments markdown="1">
</div>
