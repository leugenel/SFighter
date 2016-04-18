__author__ = 'eugenel'

import time
import quoteRest
import config
import Common

price = Common.get_quote_price()

if price == 0:
    print "No Price need try again"
    exit(0,0)

# Place a market order to buy stock:
response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, 100)
print result


Common.is_deal_done(10, response, result)