# Finite State-Machines

* [Introduction](#introduction)
* [Method](#method)
* [Example](#example)
* [The Core](#the-core)
* [Relation to Code](#relation-to-the-code)
* [Transition Graphs](#transition-graphs)
* [visio2python](#visio2python)
* [List of BitDust automata](#list-of-bitdust-automata)


## Introduction

The BitDust project is developed on the principles of [automata-based programming](https://en.wikipedia.org/wiki/automata-based_programming) and [open project documentation movement](http://is.ifmo.ru/english/).

This is a programming paradigm in which a program or its fragment is represented as a model of a [finite state machine](glossary.md#finite-state-machine).
The distinctive feature of this approach is identifying each state the process can be in, in order to analyze the program behavior as a whole.
State machine transition graphs are used at each stage of software development and in the final documentation.

SWITCH-technology of automata-based programming was first introduced by Anatoliy Abramovich Shalyto in 1991.
You are welcome to study the suggested approach in more detail on the website of the academic department of "Programming Techniques" [is.ifmo.ru](http://is.ifmo.ru/automata_en/) of the Saint Petersburg National Research University of Information Technologies, Mechanics and Optics,
and also by reading the article [Automata-based Programming](https://en.wikipedia.org/wiki/automata-based_programming)
on Wikipedia.

As a general principle, using finite state machines to implement program logic, as well as automatically compiling transition graphs into Python source code, allows the development process to be optimized considerably.


## Method

I use a slightly modified method of automata-based programming. On the arcs of the transition graphs, events, conditions and actions are marked in a format that is as close as possible to Python syntax; in addition, color keys and text formatting are used.

Compared to the classic method of Anatoliy Shalyto, my approach has some small differences:

* color differentiation helps visualization
* using function names instead of numbers creates more "talking" drawings
* you can write whole Python statements on the arcs, which opens more possibilities for the developer

Each automat is a descendant of the
[Automat](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/automats/automat.py#L256) class, which implements all key interactions in the BitDust program:

+ initializes a new state machine instance when it is created
+ terminates it cleanly
+ keeps a global index of all existing state machines
+ tracks the current state of the state machine
+ receives, sends and handles events
+ manages adjustable timers
+ manages the debug log in the program


## Example

As an example, consider a simple finite state machine which is designed to track the current status of the user’s connection to a given node in the BitDust network.

In this picture you can see an automat called
[contact_status()](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/p2p/contact_status.py#L308),
which has four states.

<div class=automatpng markdown="1">
[![contact_status()](p2p/contact_status.png)](p2p/contact_status.pdf)
</div>

It has the following elements:

<div id=table01 markdown="1">
<style>
div#table01 td, th { padding: 0px 15px; white-space: nowrap; }
div#table01 img { max-width: 100px; }
</style> 

| states         | events          | conditions     | actions           | variables     |
| :---           | :---            | :---           | :---              | :---          |
| **OFFLINE**    | outbox-packet   | isPingPacket() | doRepaint()       | AckCounter    |
| **CONNECTED**  | inbox-packet    | isDataPacket() | doRememberTime()  | &nbsp;        |
| **PING**       | file-sent       | &nbsp;         | &nbsp;            | &nbsp;        |
| **ACK?**       | sent-done       |                |                   | &nbsp;        |
|                | sent-failed     |                |                   |               |
|                | timer-20sec     |                |                   |               |

</div>

The automat `contact_status()` works as follows:

+ at the moment of creation it starts in the **OFFLINE** state
+ when it receives an incoming packet from the target node, it moves to the **CONNECTED** state and the current moment in time is "registered" to keep track of the connection duration
+ if a special service packet was sent by the program to check the current status of the connection and the condition `isPingPacket()` is triggered, the automat moves to the **PING** state and waits for a response from the remote machine
+ if the request times out or sending a packet to the target node fails, the state machine moves to the **OFFLINE** state

Proper operation of the automat helps to constantly track the current status of the connection with the given node – you just need to check the value of the `state` variable, which is a member of the `ContactStatus` class.
For instance, `self.state == 'CONNECTED'` means that the user is online at the current moment.


## The Core

All this logic is concentrated in the kernel of the finite state machine in the method [A(event, arg)](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/p2p/contact_status.py#L330)
of `ContactStatus` class:

     def A(self, event, arg):
        #---CONNECTED---
        if self.state == 'CONNECTED':
            if event == 'sent-failed' and self.Fails >= 3 and self.isDataPacket(arg):
                self.state = 'OFFLINE'
                self.doRepaint(arg)
            elif event == 'sent-failed' and self.isDataPacket(arg) and self.Fails < 3:
                self.Fails += 1
        #---OFFLINE---
        elif self.state == 'OFFLINE':
            if event == 'outbox-packet' and self.isPingPacket(arg):
                self.state = 'PING'
                self.AckCounter = 0
                self.doRepaint(arg)
            elif event == 'inbox-packet':
                self.state = 'CONNECTED'
                self.Fails = 0
                self.doRememberTime(arg)
                self.doRepaint(arg)
        #---PING---
        elif self.state == 'PING':
            if event == 'sent-done':
                self.state = 'ACK?'
                self.AckCounter = 0
            elif event == 'inbox-packet':
                self.state = 'CONNECTED'
                self.Fails = 0
                self.doRememberTime(arg)
                self.doRepaint(arg)
            elif event == 'file-sent':
                self.AckCounter += 1
            elif event == 'sent-failed' and self.AckCounter > 1:
                self.AckCounter -= 1
            elif event == 'timer-20sec' or (event == 'sent-failed' and self.AckCounter == 1):
                self.state = 'OFFLINE'
                self.doRepaint(arg)
        #---ACK?---
        elif self.state == 'ACK?':
            if event == 'inbox-packet':
                self.state = 'CONNECTED'
                self.Fails = 0
                self.doRememberTime(arg)
                self.doRepaint(arg)
            elif event == 'timer-20sec':
                self.state = 'OFFLINE'
            elif event == 'outbox-packet' and self.isPingPacket(arg):
                self.state = 'PING'
                self.AckCounter = 0
                self.doRepaint(arg)
        return None

This code is automatically generated from the transition graph vector diagram of the finite state machine, so you do not need to write all these lines by hand and have no chance to make a mistake.
The source files of the project can be automatically updated after any modifications to the finite state machine; how this works is described below.

Within the concept of open project documentation, the transition graphs are used not only at the design and development stage, but also in the documentation and product description. This helps eliminate errors in programming logic – with this automation, the working code becomes absolutely identical to the visual representation of the finite automat. Also it helps all sides to understand each other more clearly: customers, developers, testers, end-users.

This allows the software development process to be split into at least two paths and significantly optimizes the whole working process on the project:

+ behavior design of the program
+ functional development and tests


## Relation to the Code

Let's look at the example below: the given method
[doRememberTime()](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/p2p/contact_status.py#L395)
of `ContactStatus` class records the current moment in time – this is exactly the part of the functionality that is managed by the finite automat:

    def doRememberTime(self, arg):
        self.time_connected = time.time()
        
This is very simple code, but it performs a useful action and calls external code - actions and conditions become separated from the state machine and the target logic.

For every new network connection a new single instance of this automat is created; the method
[A(idurl, event, arg)](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/p2p/contact_status.py#L292)
creates new instances and refers to existing instances of the automat.

External calls to the automat are made through [automat(event, args)](https://github.com/bitdust-io/public/blob/fd536b01983f419030fa070b95d18c11da502b46/automats/automat.py#L425) 
method of the `Automat` class; for example, after a new incoming packet is received from the target node, an `inbox-packet` event is passed to the state machine:

    def Inbox(newpacket, info, status, message):
        A(newpacket.OwnerID, 'inbox-packet', (newpacket, info, status, message))
        ...
        
In other words, we can separate useful logic from the rest of the code during development and also structure the key interactions throughout the software. This depends on the developer and their understanding of the whole process.

In fact, there is no need to create state machines just for the sake of it. In my understanding, the purpose of automata-based programming is to highlight the key abstractions and processes described in the program and make their logic easier to understand.

In the future, you can always go back and instantly remember how this piece of code works and very easily change the program behaviour. The majority of the BitDust code is implemented using traditional programming methods, and state machines are used only for constructing the top-level classes. As usual, the best product is obtained when a balance is struck.

This approach reduces the likelihood of logic errors in the program almost to zero, while troubleshooting is in most cases the most complex and time-consuming process at the development and testing stage. As a rule, the functionality of the software is divided into multiple methods, which can be programmed and tweaked separately or in a specially created test environment with the use of different automatic test and tweak procedures. 


## Transition Graphs

A transition graph is a graphical representation of the multiple states of the automat and the transitions between them. In the visual representation of the finite state machine you can see the logic of the algorithm and all the possible process stages, outcomes and interconnections. States and transitions form the behavioral model of the program that controls a specific unit or process.

A state is the key element of the finite automat: it separates the stages of the algorithm. While the program runs, the automat makes transitions between its states. It can get into the same state several times or, on the contrary, never get into some predefined state.

Before a transition from one state to another, the condition assigned to that transition is tested. The condition can be written as a statement in Python and can consist of function invocations, access to variables or status inspection of other automats.

If the condition is met, the transition to the other state is made and the actions assigned to this transition are taken. These may include functions, Python statements or invocations of other finite state machines.

All interactions of the finite state machine are done by receiving and sending events. They are passed directly into the automat kernel and trigger the check of transitions between states.

Events, conditions and actions form the final statement of the transition function from one state to another. Below are examples of elements that can be used to write these statements on the transition graph:


| element   | example |                    
| :---      | :--- |
| event     | inbox-packet | 
|           | contact_status.state is PING |
|           | timer-30sec |
| condition | isDataPacket() |
|           | AckCounter>1 |
|           | sent-failed and AckCounter==1 |
| action    | doRepaint() |
|           | AckCounter=0 |
|           | Attempts+=1 |
|           | contact_status(init) |



## visio2python

Microsoft Visio 2007 is used to create the vector diagrams of transition graphs. Transition graphs of finite state machines, which control the behavior of BitDust client software, reside in *.vsd files.

A small tool called [visio2python](https://github.com/vesellov/visio2python/blob/master/README.md) was developed; it optimizes and facilitates the development of programs that use finite state machines.
It can translate transition graphs created in Microsoft Visio into Python or JavaScript code.

[https://github.com/vesellov/visio2python](https://github.com/vesellov/visio2python)


## List of BitDust automata

Below is a list of state machines currently used in the BitDust software.
You can click on any item in the list to look at the transition graph of the state machine.

* [backup()](automat_backup.md)
* [backup_db_keeper()](automat_backup_db_keeper.md)
* [backup_monitor()](automat_backup_monitor.md)
* [backup_rebuilder()](automat_backup_rebuilder.md)
* [contact_status()](automat_contact_status.md)
* [customers_rejector()](automat_customers_rejector.md)
* [data_sender()](automat_data_sender.md)
* [fire_hire()](automat_fire_hire.md)
* [id_registrator()](automat_id_registrator.md)
* [id_restorer()](automat_id_restorer.md)
* [id_server()](automat_id_server.md)
* [initializer()](automat_initializer.md)
* [install_wizard()](automat_install_wizard.md)
* [installer()](automat_installer.md)
* [list_files_orator()](automat_list_files_orator.md)
* [local_service()](automat_local_service.md)
* [network_connector()](automat_network_connector.md)
* [network_transport()](automat_network_transport.md)
* [nickname_holder()](automat_nickname_holder.md)
* [nickname_observer()](automat_nickname_observer.md)
* [p2p_connector()](automat_p2p_connector.md)
* [packet_in()](automat_packet_in.md)
* [packet_out()](automat_packet_out.md)
* [raid_worker()](automat_raid_worker.md)
* [restore()](automat_restore.md)
* [shutdowner()](automat_shutdowner.md)
* [stun_client()](automat_stun_client.md)
* [stun_server()](automat_stun_server.md)
* [supplier_connector()](automat_supplier_connector.md)
* [supplier_finder()](automat_supplier_finder.md)
* [tcp_connection()](automat_tcp_connection.md)
* [udp_connector()](automat_udp_connector.md)
* [udp_node()](automat_udp_node.md)
* [udp_session()](automat_udp_session.md)
* [udp_stream()](automat_udp_stream.md)

