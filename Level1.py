__author__ = 'eugenel'

import time
import config #internal project configuration
import sys
import Common
import quoteRest

# We need to buy 100 000 shares - lets go to 500 for one buy
sleep_time = 3  # sec
num_iterations = 100
num_shares = 1000

for num in range(1, 100):
    # Receive first quote and price
    price = Common.price_loop(sleep_time, num_iterations)
    print price
    if price == 0:
        print "No Price ---> need to try again"
        sys.exit()
    # Place a market order to buy stock: qty=num_shares
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, num_shares)
    print result
    if not Common.is_deal_done(num_iterations, response, result):
        print "We fail on this deal"
        break
    time.sleep(2)

