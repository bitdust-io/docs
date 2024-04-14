# BitDust Crypto Contracts

(in progress)

* [Business requirements](#business-requirements)



## Business requirements

BitDust do not have (and do not need) own currency - we count hardware resources, not euros, bucks or BitCoins. However to be able to buy/sell PC resources, of course, necessary to implement some "coins". There are several important points needs to be considered in this topic:

+ Because of distributed design of whole BitDust eco-system all billings and payments must be fully decentralized/distributed as well. That means there should not exist one single point of interest - nobody should be able to control and manage all billing operations in the network and collect/centralize customer information.

+ Imagine a situation when one customer is located in country A and using storage provided from supplier living in country B. This customer able to pay in local currency for country A, but supplier would like to receive money in another currency, because he live in country B where currency A is not available. So the method must be independent and generic.

+ Transfer/storage costs for each and every single small transaction must be very low, need to reduce amount of regular transactions as much as possible. For example one customer have 64 suppliers and paying all of them one by one individually is not efficient at all - he will prefer to pay only once for all finished contracts or even with fixed-price.

+ It must be possible to use BitDust network without spending any real cash - if you donate more resources than you consume all services must be free for you.

+ It must be possible to reward developers.



Based on these requirements we started desiging and developing a distributed online payment system for BitDust project. The goal is to allow users to gain some "coins" and benefit from providing resources of own PC's to other people.

