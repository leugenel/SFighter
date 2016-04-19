__author__ = 'eugenel'

import time
import config #internal project configuration
import sys
import Common
import quoteRest

# Receive initial price - may be as the last ask
# Set dictionary {} of IDs, counter - 10 every time
# each buy object will have the initial price-50
# set to buy 10 such object with qty 100 - 1000 all
# set sleep(0.3) inside the loop that check this list
# if it done add the new object with the saled price-50
# if counter == 10 then close this buy and add the new with price+50
# always verify the bayed qty against 100000
# finish when buy 100000 shares

# We need to buy 100 000 shares - lets go to 500 for one buy
sleep_time = 0.3  # sec
num_iterations = 10
number_bids = 11
num_shares = 100
bid_list = {}
price_list = []

# Preparing first time
price = Common.price_loop(sleep_time, num_iterations)
if price == 0:
    print "No Price ---> need to try again"
    sys.exit()

for i in range(1, number_bids):
    # Place a market order to buy stock: qty=num_shares
    if price > 50:
        price -= 50
    price_list.append(price)
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, num_shares)
    if response != 200:
        print response
        sys.exit()
    print result
    bid_list[result['id']] = 1

print price_list
# Now the big iteration
max_buy_value = 100000
buy_value = 0
while buy_value < max_buy_value:
    # Verify bids status
    for key, value in bid_list.iteritems():
        if quoteRest.get_order_status(config.venue, config.stock, key): # Done was buy
            buy_value += num_shares
            value = num_iterations+1 # value more than maximum counter, we mark the bid that need be deleted
        else:
            value += 1
        time.sleep(sleep_time)
    print bid_list
    # Clean bid list
    i = 0
    for key, value in bid_list.items():
        if value == num_iterations:
            price_list[i] += 50
        else:
            if price_list[i] > 50:
                price_list[i] -= 50
        del bid_list[key]
        i += 1
    print price_list
    for i in range (len(price_list)):
        response, result = quoteRest.set_order(config.venue, config.stock, config.account, price_list[i], num_shares)
        if response != 200:
            print response
            sys.exit()
        print result
        bid_list[result['id']] = 1

    print bid_list
    time.sleep(sleep_time)
