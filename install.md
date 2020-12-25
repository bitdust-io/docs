# Install BitDust software


* [About](#about)
* [Install software dependencies](#install-software-dependencies)
* [Get BitDust to your local machine](#get-bitdust-to-your-local-machine)
* [Building virtual environment](#building-virtual-environment)
* [Run BitDust](#run-bitdust)
* [Binary Dependencies](#binary-dependencies)



## About

#### Decentralized encrypted storage platform

The lack of secure storage is a problem for Internet users. BitDust decentralized encrypted storage platform solves this problem by providing users the ability to store their data fully encrypted on a decentralized network via an easy-to-use application. Providing them the ability to share data only with trusted contacts.

All your data is encrypted before it leaves your computer with a private key that your computer generates. No one else can read your data, not even the BitDust Team! 

BitDust is written in Python using pure Twisted framework and published under GNU AGPLv3.

There is an early alpha version available for Windows, Mac and Linux. Any feedback in regards to this alpha version is much appreciated. Please provide your feedback to info@bitdust.io .


## Install software dependencies

Under Ubuntu/Debian, and probably most other distros as well, you can install all dependencies with single command:

        sudo apt-get install git gcc python3-dev python3-virtualenv


Optionally, you can also install [miniupnpc](http://miniupnp.tuxfamily.org/) tool if you want BitDust automatically set up UPnPc configuration of your network router so it can also accept incomming connections from other nodes.:

        sudo apt-get install miniupnpc


On MacOSX platform you can install requirements with that command:

        brew install git python3


Then you need to use pip manager to get all required packages:

        pip install --upgrade --user
        pip install --upgrade pip --user
        pip install virtualenv --user


On Raspberry PI you will need to install those packages:

        sudo apt-get install git gcc python3-dev python3-virtualenv python3-pip libffi-dev libssl-dev



## Get BitDust sources to your local machine

Second step is to get the BitDust sources. To have full control over the BitDust process running on your local machine you can better make a fork of the Public BitDist repository on GitHub at https://github.com/bitdust-io/public and clone it on your local machine:

        git clone https://github.com/<your GitHub username>/<name of BitDust fork>.git bitdust


The software will periodically run `git fetch` and `git rebase` to check for recent commits in the repo. This way we make sure that everyone is running the latest version of the program. Once you made a fork, you will have to update your Fork manually and pull commits from the Public BitDust repository if you trust them.

However if you just trust BitDust contributors you can simply clone the Public repository directly and software will be up to date with the "official" public code base:

        git clone https://github.com/bitdust-io/public.git bitdust



## Building virtual environment

Afterwards you will need to build virtual environment with all the required Python dependencies, making sure BitDust software will run fully isolated.

Single command should make it for you, all required files will be generated in the `~/.bitdust/venv/` folder:

        cd bitdust
        python3 bitdust.py install


Last step to make BitDust software ready to be used is to make a short alias in your OS, then you can just type `bitdust <some command>` in command line to get fast access to the program:
        
        sudo ln -s -f /home/<user>/.bitdust/bitdust /usr/local/bin/bitdust  # location depend on your system



## Run BitDust

Start using the software by creating an identity for your device in BitDust network:
       
        bitdust id create <some nick name>
       

I recommend you to create another copy of your Private Key in a safe place to be able to recover your data in the future. You can do it with this command:

        bitdust key copy <nickname>.bitdust.key


In the future, just in case you need to restore access to your data, you will need to install BitDust again and recover your identity:

        bitdust id restore <nickname>.bitdust.key


Your settings and local files are located in this folder: `~/.bitdust/`

Type this command to read more info about BitDust commands:

        bitdust help


To run the software type:

        bitdust
        

Start as background process:

        bitdust detach


To get some more insights or just to know how to start playing with software
you can visit [BitDust Commands](commands.md) page. 

To get more info about all API methods served by BitDust engine process go to [BitDust API](api.md) page.



## Binary Dependencies

If you are installing BitDust on Windows platforms, you may require some binary packages already compiled and packaged for Microsoft Windows platforms, you can check following locations and download needed binaries and libraries:

* cygwin: [cygwin.com](https://cygwin.com/install.html)
* git: [git-scm.com](https://git-scm.com/download/win)
* python2.7 or python3: [python.org](http://python.org/download/releases)
* twisted: [twistedmatrix.com](http://twistedmatrix.com)
* pyasn1: [pyasn1.sourceforge.net](http://pyasn1.sourceforge.net)
* miniupnpc: [miniupnp.tuxfamily.org](http://miniupnp.tuxfamily.org/)



<div class=fbcomments markdown="1">
</div>
