__author__ = 'eugenel'

import json
import httplib
import time
import config #internal project configuration

account = "HAH71340638"
venue = "MKPEX"
stock = "ICKI"

#Get the quote price
def getTheQuotePrice(priceDecrise):
    connection = httplib.HTTPSConnection(config.site)
    connection.request("GET", "/ob/api/venues/"+venue+"/stocks/"+stock+"/quote", headers=config.head)
    response = connection.getresponse()
    price=0
    if(response.status==200):
        result = json.loads(response.read())
        print result
        price=result['bid']-priceDecrise
    else:
        print response.status
    connection.close()
    return price

#Get Order status returns true if closed and false if still open
def getOrderStatus(orderID):
    connection = httplib.HTTPSConnection(config.site)
    connection.request("GET", "/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+str(orderID), headers=config.head)
    order_response=connection.getresponse()
    if(order_response.status==200):
        result=json.loads(order_response.read())
        print result
        connection.close()
        if(not result['open']):
            return True
    else:
        print order_response.status
    return False

price=getTheQuotePrice(50)

#Place a market order to buy stock:
connection = httplib.HTTPSConnection(config.site)
order = {"account":account,"price":price,"qty":100,"direction":"buy","orderType":"limit"}

connection.request("POST","/ob/api/venues/"+venue+"/stocks/"+stock+"/orders",json.dumps(order),config.head)
response = connection.getresponse()

#Verify that the deal is Done
if(response.status==200):
    result = json.loads(response.read())
    connection.close()
    print result
    if(result['ok'] and result['open']):
        Counter=0
        while(Counter<10):
            # connection = httplib.HTTPSConnection(config.site)
            # connection.request("GET", "/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+str(result['id']), headers=config.head)
            # order_response=connection.getresponse()
            # if(order_response.status==200):
            #     result=json.loads(order_response.read())
            #     print result
            #     if(not result['open']):
            #         print "DONE!"
            #         break
            # else:
            #     print order_response.status
            if(getOrderStatus(result['id'])):
                break
            Counter+=1
            #connection.close()
            time.sleep(3)
else:
    print response.status
if (Counter==10):
    print "NOT SAILED"