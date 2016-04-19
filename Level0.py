__author__ = 'eugenel'

import sys
import quoteRest
import config
import Common

sleep_time = 3
num_iterations = 10
price=Common.price_loop(sleep_time, num_iterations)
if price == 0:
    print "No Price need try again"
    sys.exit()

# Place a market order to buy stock:
response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, 100)
print result

num_iterations=10
sleep_time = 3
if Common.is_deal_done(num_iterations, response, result, sleep_time):
    print "DEAL DONE!"
else:
    print "NO DEAL!"