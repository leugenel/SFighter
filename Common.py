__author__ = 'eugenel'

import quoteRest
import config
import time

def get_quote_price():
    response, result = quoteRest.quote_quick(config.venue, config.stock)
    price=0
    if response == 200:
        print result
        price = result['last']
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
