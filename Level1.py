__author__ = 'eugenel'

import json
import httplib
import config #internal project configuration


connection = httplib.HTTPSConnection(config.site)

account = "YS36942955"
venue = "OEGEX"
stock = "WHC"

#Place a market order to buy stock:
order = {"account":account,"price":2000,"qty":100,"direction":"buy","orderType":"limit"}

connection.request("POST","/ob/api/venues/"+venue+"/stocks/"+stock+"/orders",json.dumps(order),config.head)
response = connection.getresponse()

if(response.status==200):
    result = json.loads(response.read())
    #print response.read()
    if(result['ok']):
        print "OK"