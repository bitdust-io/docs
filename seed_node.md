# Running BitDust seed node

Here is a step-by-step guide on how to start a full BitDust node that supports other nodes in the network and acts as a "seed" node.

You need to own a domain name whose DNS records already point to your server.

For example, if you have just started with a new Ubuntu server and logged in as the `root` user, first create another user account to be able to run BitDust as a normal user without root privileges:

        adduser bitdust
        usermod -aG sudo bitdust
        logout


Now log in to your server as the `bitdust` user (not as `root`) and do not forget to set up proper SSH access with your public/private key. Remember, the BitDust software does not require root permissions to run, and no one else can provide you with more privacy than you can arrange by yourself:

        ssh bitdust@my-domain-name.com


Read more about [BitDust installation](install.md) or just follow the few steps below.

First, clone the BitDust sources locally:

        git clone https://github.com/bitdust-io/public.git bitdust


Create the BitDust virtual Python environment:
        
        cd bitdust
        python3 bitdust.py install


Make sure the `bitdust` command already exists so you can access BitDust from your command line shell.
You only need to do this once: create an "alias" in your global system commands list. Then you can just type `bitdust <some command>` to talk to BitDust quickly. To create a system-wide shell command, you can manually copy the already existing script `/home/bitdust/.bitdust/bitdust` to your PATH and it will work right away. Another very simple way is to just create a symlink:

        sudo ln -s -f /home/bitdust/.bitdust/bitdust /usr/local/bin/bitdust


A few services need to be enabled; by default they are turned off because normal users will most probably act as customers/consumers at the beginning.

Switch ON the identity server on your node so you help other people to identify themselves in the network - other users will store their identities on your host:

        bitdust set services/identity-server/enabled true
        bitdust set services/identity-server/host my-domain-name.com
        bitdust set services/identity-server/tcp-port 6661
        bitdust set services/identity-server/web-port 8084


The BitDust software is supposed to run without root privileges, so it cannot open and listen on port 80. A bit more configuration is needed to redirect external requests to the server on port 80 to the BitDust software listening on port 8084: read more about [Identity server configuration](identity_server.md) to know how to arrange it in a few steps.

Set the UDP port number for your DHT seed:

        bitdust set services/entangled-dht/udp-port 14441


Disable the proxy-transport and customer services, because you do not need them when starting a provider node:

        bitdust set services/proxy-transport/enabled false
        bitdust set services/customer/enabled false


To make it clearer for other users of your seed node, we advise you to use an identifier format based on the DNS name of that machine: `seed_my_domain_name_com@my-domain-name.com`.

To do that, you need to set the domain name of your seed node in the settings before you create a new identity:

        bitdust set services/identity-propagate/known-servers my-domain-name.com:80:6661


Start BitDust in the background:

        bitdust daemon


Now you can interact with the BitDust software running on your local machine via the HTTP REST API. Let's create a new identity for your seed node:

        curl -X POST -d '{"username": "seed_my_domain_name_com"}' localhost:8180/identity/create/v1


Make sure you also back up your private key and copy it to a safe place.

        curl -X POST -d '{"destination_path": "/tmp/bitdust_identity_backup.txt"}' localhost:8180/identity/backup/v1
        mv /tmp/bitdust_identity_backup.txt /media/USB_drive/


Restart BitDust and enjoy: your identity should be accessible at `http://my-domain-name.com/seed_my_domain_name_com.xml` if all steps were correct.

        bitdust restart


To make life easier you can also configure BitDust to start automatically when your machine reboots. For example, on a Debian system you can use the `crontab` tool for that:

        crontab -e
        @reboot /usr/local/bin/bitdust daemon


If you plan to maintain your new BitDust node for a while and support the network, it makes sense to include your node in the list of "well known" nodes, which are hard-coded in the [default_network.json](https://github.com/bitdust-io/public/blob/master/default_network.json) file.

You can fork the [Public Git Repository](https://github.com/bitdust-io/public), modify the `default_network.json` file in your forked repository and open a [Pull Request](https://github.com/bitdust-io/public/pulls) with your changes - this way we can collaborate all together and maintain a list of the most reliable BitDust seed nodes.

Contact the BitDust contributors to let them know that you have started a new seed node, and one of the developers will approve your Pull Request.

