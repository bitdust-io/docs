# Running BitDust seed node

Here is a step-by-step guide about how to start a full BitDust node that supports other nodes in the network and act as a "seed" node.

You need to own a domain name which is already pointing the DNS to your server.

For example, you just started with a new Ubuntu server and logged in as `root` user, first create another user account to be able to run BitDust as a normal user without root priviledges:

        adduser bitdust
        usermod -aG sudo bitdust
        logout


Now log in to your server as `bitdust` user (not as `root`) and do not forget to setup proper SSH access with your Public/Private key. Remember, BitDust software do not require root permissions to run, and no one else can provide you with more privacy than you can arrange by yourself:

        ssh bitdust@my-domain-name.com


Read more about [BitDust installation](install.md) or just follow those few steps bellow.

First clone BitDust sources locally:

        git clone https://github.com/bitdust-io/public.git bitdust


Create BitDust virtual Python environment:
        
        cd bitdust
        python bitdust.py install


Make sure you already have `bitdust` command existing so you can access BitDust from your command line console shell.
You only need to do this one time and create an "alias" in your global system commands list. Then you can just type: `bitsut <some command>` to be able to talk to BitDust quickly. To create system-wide shell command you can manually copy already existing script `<your home location>/.bitdust/bitdust` to your PATH and it will work right away. Another very simple way is to just create a symlink:

        sudo ln -s -f /home/<user>/.bitdust/bitdust /usr/local/bin/bitdust  # location depend on your system


Few services needs to be enabled, by default they are turned off because normal users will most probably act as a customer/consumer at the beginning.

Switch ON identity server on your node so you will help other people to identify in the network - other users will store their identities on your host:

        bitdust set services/identity-server/enabled true
        bitdust set services/identity-server/host my-domain-name.com
        bitdust set services/identity-server/tcp-port 6661
        bitdust set services/identity-server/web-port 8084


BitDust software suppose to run without root priviledges, so it can not open and listen on port 80. This will need a bit more configuration in order to redirect external requests to the server on port 80 to BitDust software listening on port 8084: read more about [Identity server configuration](identity_server.md) to know how to arrange it in a few steps.

Set UDP port number for you DHT seed:

        bitdust set services/entangled-dht/udp-port 14441


Disable proxy transport and customer service because you do not need those if starting a provider node:

        bitdust set services/proxy-transport/enabled false
        bitdust set services/customer/enabled false


To make it more clear for other users using your seed node, we advice you to use a certain identifier format which is based on DNS name of that machine: `seed_my_domain_name_com@my-domain-name.com`.

In order to do that you need to set domain name of your seed node in the settings, before you create a new identity:

        bitdust set services/identity-propagate/known-servers my-domain-name.com:80:6661


Start BitDust in background:

        bitdust daemon


Now you can interact with BitDust software running on your local machine via HTTP Rest API. Lets create a new identity for your seed node:

        curl -X POST -d '{"username": "seed_my_domain_name_com"}' localhost:8180/identity/create/v1


Make sure you also did a backup of your private key and copied that in a safe place.

        curl -X POST -d '{"destination_path": "/tmp/bitdust_identity_backup.txt"}' localhost:8180/identity/backup/v1
        mv /tmp/bitdust_identity_backup.txt /media/USB_drive/


Restart BitDust and enjoy, your identity should be accessable on `http://my-domain-name.com/seed_my_domain_name_com.xml` if all steps were correct.

        bitdust restart


To make life easier you can also configure BitDust to start automatically when your machine reboots. For example on Debian system you can use `crontab` tool for that:

        crontab -e
        @reboot /usr/local/bin/bitdust daemon


If you plan to maintain your new BitDust node for a while and support the network it makes sense to include your node into a list of "well known" nodes, which are hard-coded in [networks.json](https://github.com/bitdust-io/public/blob/master/networks.json) file.

You can Fork [Public Git Repository](https://github.com/bitdust-io/public), modify `networks.json` file in your forked repository and start a [Pull Request](https://github.com/bitdust-io/public/pulls) with your changes - this way we can collaborate all together and maintain a list of the most reliable BitDust seed nodes.

Contact the BitDust contributors to notify about this new Seed node was started by you and one of the developers will approve your Pull Request.



<div class=fbcomments markdown="1">
</div>
