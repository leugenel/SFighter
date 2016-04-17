__author__ = 'eugenel'

import time
import quoteRest

account = "SPB65525666"
venue = "SLPEX"
stock = "HYYN"

# Get the quote price
def get_quote_price():
    response, result = quoteRest.quote_quick(venue, stock)
    price=0
    if response == 200:
        print result
        price = result['last']
    else:
        print response
    return price


price = get_quote_price()

if price == 0:
    print "No Price need try again"
    exit(0,0)

# Place a market order to buy stock:
response, result = quoteRest.set_order(venue, stock, account, price, 100)
print result
# Verify that the deal is Done
Counter=0
if response == 200:
    print result
    if result['ok']:
        if result['open']:
            while Counter<10:
                if quoteRest.get_order_status(venue,stock, result['id']):
                    print "DONE!"
                    break
                Counter += 1
                time.sleep(3)
        else:
            print "WE DONE IMMEDIATELY!"

    else:
        print "The setOrder request 'ok' flag is FALSE"
else:
    print response

if Counter == 10:
    print "NOT SAILED"
else:
    print "It was " + str(Counter) + " iterations"
