__author__ = 'eugenel'

import time
import config #internal project configuration
import Common
import quoteRest

# We need to buy 100 000 shares - lets go to 500 for one buy

for num in range(1, 100):
    # Receive first quote and price
    price = Common.get_quote_price()
    print price
    if price == 0:
        print "No Price ---> need to try again"
        exit(0,0)
    # Place a market order to buy stock:
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, 1000)
    print result
    if not Common.is_deal_done(10, response, result):
        print "We fail on this deal"
        break
    time.sleep(2)

