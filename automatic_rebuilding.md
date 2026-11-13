DRAFT: a description of the future rebuilding mechanism involving the "spare supplier" and "ReBuilder" roles - not implemented yet.
Currently rebuilding is performed by the software on the customer's own device, while it is running.

1. suppliers watch each other!
    a. every minute one of the suppliers pings all other suppliers in the customer's family
    b. the next minute another supplier pings all the other suppliers, and so on
    c. if the customer is online, suppliers do not do this - the customer pings everyone and makes the decisions
    d. a supplier first pings the customer, and only if the customer is offline does it ping all the suppliers
    e. if the customer is online, the supplier will start the next ping only after n minutes, n = number of suppliers
    f. as a result, every minute the customer (if online) will receive one ping from one of the suppliers, in turn

2. all suppliers know each other!
    a. the customer informs each supplier about the whole family of suppliers every time the family changes
    b. only the customer can change the family - hire or fire a supplier (the exception is the "spare", which the suppliers hire themselves while the customer is offline, see p.3; the final decision about it is still made by the customer, see p.6)
    c. suppliers also publish their position in this customer's family in the DHT
    d. from the DHT any other node outside the family can find out the full list of all suppliers
    e. when suppliers ping each other, they also share the list of suppliers known to them - for verification
    f. it is important to minimize the number of regular requests to the DHT

3. a supplier hires a "spare" by itself when it detects that another supplier is offline!
    a. having detected another supplier that does not respond, the pinging supplier remembers it
    b. it passes the "dead" one to the next live supplier, which will ping in the next minute
    c. the next pinging supplier also detects the dead one, remembers it and passes this information on to the next one
    d. after several iterations, when several suppliers together have detected the dead one, a spare is hired

4. the spare supplier is added to this customer's family!
    a. the spare supplier is assigned to the same position as the dead supplier, but does not replace it in the family
    b. the spare supplier publishes information about itself in the DHT
    c. the spare supplier finds a "ReBuilder" to reconstruct the lost piece of the customer's data
    d. the spare supplier receives the rebuilt pieces of data from the ReBuilder and stores them like a regular supplier
    e. several ReBuilders can be started if the expected amount of data is large enough
    f. the spare also takes part in the "periodic ping" and watches the other suppliers and spares

5. the ReBuilder receives a task from the spare!
    a. the ReBuilder scans the DHT and finds out all the suppliers and spares in the family
    b. the ReBuilder pings all the suppliers and spares and starts downloading pieces of data from them
    c. block by block, the ReBuilder reassembles the lost fragments and sends them to the spare
    d. if several ReBuilders work in parallel, they take different blocks - the spare manages this

6. the customer comes back online and resolves the situation with the spares and the dead!
    a. the customer can request the "ping history" from all suppliers and spares and build a reliability rating
    b. if the dead supplier never came back online - the spare simply replaces it and stops being a spare
    c. if the dead supplier came back online, the customer can decide based on the rating who is more reliable
    d. if the dead one came back online very quickly, the spare can give up its role by itself and leave the family
    e. the customer can (unfinished)

7. the customer never comes back online at all!
    a. the suppliers and the customer agree in advance on the maximum "contract" term at the moment of first contact
    b. the spare learns the contract term of the dead supplier from the DHT and "inherits" the same "contract" term
    c. after their contracts expire, suppliers and spares automatically leave the family and the data will be lost
