__author__ = 'eugenel'

import quoteRest
import config
import time
import logging


def get_quote_price():
    response, result = quoteRest.quote_quick(config.venue, config.stock)
    price=0
    if response == 200:
        plog_info("get_quote_price() - result")
        plog_info(result)
        if result['askSize']==0 or result['bidSize']==0:
            return price
        else:
            price = int(result['ask']) #(result['bid']+result['ask'])/2
    else:
        plog_info(response)
    return price

# Verify that the deal is Done
def wait_for_close(num_iterations, result_id, sleep_time):
    counter=0
    while counter<num_iterations:
        if quoteRest.get_order_status(config.venue, config.stock, result_id):
            plog_info("DONE!")
            break
        counter += 1
        time.sleep(sleep_time)
    return counter

# Verify that the deal is Done
def is_deal_done(num_iterations, response, result, sleep_time):
    done = False
    counter=0
    if response == 200:
        plog_info(result)
        if result['ok']:
            if result['open']:
                counter = wait_for_close(num_iterations, result['id'], sleep_time)
            else:
                plog_info("WE DONE IMMEDIATELY!")
                done = True
        else:
            plog_info("The setOrder request 'ok' flag --> FALSE")
    else:
        plog_info(response)

    if counter == num_iterations:
        plog_info("NOT SAILED")
    else:
        plog_info("It was " + str(counter) + " iterations")
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

def plog_info(message):
    print message
    logging.info(message)
