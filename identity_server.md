# How to start a new Identity Server in BitDust network


## Intro

You need to create new identity for your own to be able to communicate with other nodes and access BitDust community.
Identity files are distributed across identity servers in the network, other nodes holding and exposing copies of your identity.

The third node can access that ID server and download your identity to be able to talk to you.
So any node in the network can start own ID server and help to maintain network and make it more reliable.

Your global IDURL is formed based on your nickname and DNS name (or IP address) of the first ID server.

When one of your Identity servers is down, BitDust software will automatically find a fresh Identity server for you and "propagate" your identity there and also remove dead Identity server from the list of your sources. That process is called "identity rotate" and it is fully automated and decentralized.

Because of that BitDust network authentication is actually pretty reliable and fully independent for any single party.


## Install and configure a web-server

To protect your BitDust node from outside we can use a web-server and re-route traffic internally to the `bitdust` process.

Here are two example configurations for well-known servers: `Apache2` and `Nginx`.
But first, you need to setup a hostname on your machine if you did not do it before:

        sudo hostname -b my-own-identity-server.com


#### Nginx setup

Install Nginx with Apt:

        sudo apt-get update
        sudo apt-get install nginx


Disable the default virtual host, that is pre-configured when Nginx is istalled via Ubuntu packet manager apt:

        sudo unlink /etc/nginx/sites-enabled/default


Enter the directory /etc/nginx/sites-available and create a configuration file:

        cd /etc/nginx/sites-available
        sudo nano my-own-identity-server_com.conf


You can use bellow sample config:

        server {
            server_name my-own-identity-server.com www.my-own-identity-server.com;
            listen 80;
            listen [::]:80;
            access_log /var/log/nginx/idserver-log.log;
            error_log /var/log/nginx/idserver-error.log;
            location / {
                proxy_pass http://127.0.0.1:8084/;
            }
        }


Copy the configuration from /etc/nginx/sites-available to /etc/nginx/sites-enabled. It is recommended to use a symbolic link.

        ln -s /etc/nginx/sites-available/my-own-identity-server_com.conf /etc/nginx/sites-enabled/my-own-identity-server_com.conf


Enable Nginx system service and start the web-server:

        sudo systemctl enable nginx
        sudo systemctl start nginx
        sudo service nginx reload


#### Apache2 setup

Install Apache2 server if you do not have it yet on your machine:

        sudo apt-get update
        sudo apt-get install apache2


Edit Apache2 main config file:
    
        sudo nano /etc/apache2/apache2.conf 


You need to add a line to set your domain name:
    
        ServerName my-own-identity-server.com


Create a new `.conf` file for Apache2:

        sudo nano /etc/apache2/conf-available/my-own-identity-server_com.conf


Use that template to create Apache2 config, basically you can just copy & paste and only change domain name here:

        <VirtualHost *:80>
          ServerName my-own-identity-server.com
          ServerAlias www.my-own-identity-server.com
          ProxyPreserveHost on
          ProxyRequests Off
          RewriteEngine on
          ProxyPass / http://localhost:8084/
          ProxyPassReverse / http://localhost:8084/
          Redirect / http://localhost:8084/
          RewriteRule ^/(.*) http://localhost:8084/$1 [P,L]
        </VirtualHost>


Enable this configuration in apache2, run command:

        sudo a2enconf my-own-identity-server_com


Configure proxy_http and rewrite modes in apache2, run commands:

        sudo a2enmod proxy_http 
        sudo a2enmod rewrite


Now restart apache2 server:

        sudo service apache2 restart



## Configure BitDust software

First you need to [install BitDust](install.md) on your machine. 

Now configure BitDust on your node to set domain name for this new identity server, run commands:

        bitdust set services/identity-server/host my-own-identity-server.com
        bitdust set services/identity-server/enabled true


You can manually set a port number for incoming connections using such command:

        bitdust set services/identity-server/web-port 8084



## Run standalone Identity Server

Run this command to start Identity server process in current terminal:

        bitdust identity server start


Now open your favority WEB browser and navigate to [my-own-identity-server.com](my-own-identity-server.com). You should see an empty page with title "Identities on my-own-identity-server.com".

Congratulations! You are running your own identity server now and able to register your own identity there or help other people by hosting their identity files on your machine.


## Run Identity Server as daemon process

Be sure network service identity_server is enabled in settings (check configuration above) and start BitDust software in "daemon" mode:

        bitdust daemon


Be sure ID server is up and running:

        bitdust states | grep id_server
        36: id_server(LISTEN)


Open your browser and go to [my-own-identity-server.com](my-own-identity-server.com) to check server status.

To make life easier you can also configure BitDust to start automatically when your machine reboots. For example on Debian system you can use `crontab` tool for that:

        crontab -e
        @reboot /usr/local/bin/bitdust daemon


## Create dedicated identity

Normally, when you creating a new identity, software will do all stuff for you automatically and just select few random ID servers, ping them and "propagate" your new identity to those nodes.

But you can decide which ID servers you prefer, in case if you would like to control where your identity will be distributed exactly, and modify your "known" ID servers:

    bitdust set services/identity-propagate/known-servers first-server.com:80:6661,second-host.net:8080:6661


Now if you create a new identity with such commands:

    bitdust id erase
    bitdust id create my_dedicate_identity


it will be automatically "propagated" to `first-server.com` and `second-host.net` and your global IDURL should look like that: `"http://first-server.com/my_dedicate_identity.xml"`



## Support BitDust network

Contact with BitDust team to notify about this new ID server was started on your machine and we will add your domain name in the file __known_servers.py__ storing list of all known BitDust identity servers: 

* [mirror on GitHub](https://github.com/bitdust-io/devel/blob/master/userid/known_servers.py)
* [mirror on dev.bitdust.io](https://dev.bitdust.io/code/devel/blob/master/userid/known_servers.py)

You can Fork BitDust [development repository](https://dev.bitdust.io/code/devel) and open a Pull Request to modify the list of known servers in place.

