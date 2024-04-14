# Running BitDust supplier node


Supplier is a guy who donates part of storage from own PC and share resources to other users in the network.

At the moment there is no way to reward suppliers for the contribution they are doing to the network, but this is planned to come later.

Read more about [BitDust installation](install.md) or just follow those few steps bellow to install software on your machine.


First clone BitDust sources locally:

        git clone https://github.com/bitdust-io/public.git bitdust


Create BitDust virtual Python environment:
        
        cd bitdust
        python3 bitdust.py install


Last step to make BitDust software ready to be used is to make a short alias in your OS, then you can just type `bitdust <some command>` in command line to get fast access to the program:
        
        sudo ln -s -f /home/<user>/.bitdust/bitdust /usr/local/bin/bitdust  # location depend on your system


Now you need to configure few software settings to actually donate storage space to the network.

Disable services you do not need if you run supplier role. Switch off "customer service" so your machine will not consume any storage, but only donate:

        bitdust set services/customer/enabled false


Declare how much space you are willing to donate to the BitDust network:

        bitdust set services/supplier/donated-space 20GB


If you did not yet created an identity for your device in the BitDust network you can do it with such command:

        bitdust id create <some nick name>


When you did it for the first time I recommend you to create another copy of your Private Key in a safe place to be able to recover your identity in BitDust in the future. You can make a backup copy with such command:

        bitdust key copy <nickname>.bitdust.key


Finaly start BitDust software in daemon mode so it will keep running in background and you can keep using your PC:

        bitdust daemon


You can always check current situation regarding your "donated storage" with such command:

        bitdust storage

