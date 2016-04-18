__author__ = 'eugenel'

import quoteRest
import config
import time
import sys

def get_quote_price():
    response, result = quoteRest.quote_quick(config.venue, config.stock)
    price=0
    if response == 200:
        print result
        if result['askSize']==0 or result['bidSize']==0:
            return price
        else:
            price = (result['bid']+result['ask'])/2
    else:
        print response
    return price

# Verify that the deal is Done
def wait_for_close(num_iterations, result_id):
    counter=0
    while counter<num_iterations:
        if quoteRest.get_order_status(config.venue, config.stock, result_id):
            print "DONE!"
            break
        counter += 1
        time.sleep(3)
    return counter

# Verify that the deal is Done
def is_deal_done(num_iterations, response, result):
    done = False
    counter=0
    if response == 200:
        print result
        if result['ok']:
            if result['open']:
                counter = wait_for_close(num_iterations, result['id'])
            else:
                print "WE DONE IMMEDIATELY!"
                done = True
        else:
            print "The setOrder request 'ok' flag --> FALSE"
    else:
        print response

    if counter == num_iterations:
        print "NOT SAILED"
    else:
        print "It was " + str(counter) + " iterations"
        done = True
    return done

def price_loop(sleep_time, num_iterations):
    price=0
    for i in range (1,num_iterations):
        price = get_quote_price()
        if price > 0:
            break
        time.sleep(sleep_time)
    return price