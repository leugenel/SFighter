__author__ = 'eugenel'
import json
import httplib
# internal project configuration
import config

def quote_quick(venue, stock):
    connection = httplib.HTTPSConnection(config.site)
    connection.request("GET", "/ob/api/venues/"+venue+"/stocks/"+stock+"/quote", headers=config.head)
    response = connection.getresponse()
    result = None
    if response.status == 200:
        result = json.loads(response.read())
    connection.close()
    return response.status, result


# Get Order status returns true if closed and false if still open
def get_order_status(venue, stock, orderID):
    connection = httplib.HTTPSConnection(config.site)
    connection.request("GET", "/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+str(orderID), headers=config.head)
    response=connection.getresponse()
    if response.status == 200:
        result=json.loads(response.read())
        connection.close()
        if not result['open'] :
            return True
    else:
        connection.close()
    return False


def set_order(venue, stock, account, price, qty, direction="buy"):
    connection = httplib.HTTPSConnection(config.site)
    order = {"account":account,"price":price,"qty":qty,"direction":direction,"orderType":"limit"}
    connection.request("POST","/ob/api/venues/"+venue+"/stocks/"+stock+"/orders",json.dumps(order),config.head)
    response = connection.getresponse()
    result = None
    if response.status == 200:
        result = json.loads(response.read())
    connection.close()
    return response.status, result


def cancel_order(venue, stock, orderID):
    connection = httplib.HTTPSConnection(config.site)
    connection.request("DELETE", "/ob/api/venues/"+venue+"/stocks/"+stock+"/orders/"+str(orderID), headers=config.head)
    response=connection.getresponse()
    result = None
    if response.status == 200:
        result=json.loads(response.read())
    connection.close()
    return response.status, result