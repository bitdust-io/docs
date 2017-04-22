# Start a new Identity Server in BitDust network


## Install and configure apache2


Lets setup a hostname on your machine if you did not do it before:

    sudo hostname -b my-own-identity-server.com

And you will need to install Apache server if you do not have it yet on your machine:

    sudo apt-get install apache2

Edit file:
    
    /etc/apache2/apache2.conf 

you need to add a line to set your domain name:
    
    ServerName my-own-identity-server.com

Create a new my-own-identity-server_com.conf file in /etc/apache2/conf-available/ :

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

First you need to install [BitDust software](https://bitdust.io/install.html) on your machine. 

Now configure BitDust on your node to set domain name for this new identity server, run commands:

    bitdust set services/id-server/host my-own-identity-server.com
    bitdust set services/id-server/enabled true
    

You can manually set a port number for incoming connections using such command:

    bitdust set services/id-server/web-port 8084


Restart BitDust software:

    bitdust restart


Be sure ID server is up and running:

    bitdust states | grep id_server
    36: id_server(LISTEN)


Open your browser and go to http://my-own-identity-server.com or (http://localhost:8084) to check it end-to-end.


## Support BitDust network

Contact with BitDust team to notify about this new ID server was started by you and we will add your domain name in the list of [known_servers.py](http://gitlab.bitdust.io/stable/bitdust.latest/blob/master/userid/known_servers.py).


<div class=fbcomments markdown="1">
</div>
