__author__ = 'eugenel'
import time
import config
import sys
import Common
import quoteRest
import logging

logging.basicConfig(filename='level2.log',level=logging.DEBUG)
sleep_time = 0.1  # sec
num_iterations = 10
number_bids = 10
num_shares = 400
sell_list = {}
#price_list = []

while True:
    # Try buy 400 shares
    price = Common.price_loop(sleep_time, num_iterations)
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, price, num_shares)
    if response != 200:
        Common.plog_info(response)
        sys.exit()
    Common.plog_info("Set order for buy:")
    Common.plog_info(result)

    # Verify that buying works
    buy_done=False
    for i in range (1, num_iterations):
        if quoteRest.get_order_status(config.venue, config.stock, result['id']):
            buy_done=True
            break
        time.sleep(sleep_time)

    # Cancel order if not buy it
    if not buy_done:
        quoteRest.cancel_order(config.venue, config.stock, result['id'])
        Common.plog_info("Cancel buy order")
        # Lets try new buying
        continue

    #Now selling
    update_price = 100
    price_delta = 10
    sell_done = False
    for j in range (1, num_iterations):
        update_price -= price_delta
        response, result = quoteRest.set_order(config.venue, config.stock, config.account, price+update_price, num_shares, "sell")
        if response != 200:
            Common.plog_info(response)
            sys.exit()
        Common.plog_info("Set order for sell:")
        Common.plog_info(result)
        if quoteRest.get_order_status(config.venue, config.stock, result['id']):
            sell_done = True
            Common.plog_info("Sell done for price "+str(price+update_price))
            break
        time.sleep(sleep_time)
    if not sell_done:
        sell_list[result['id']]=price+update_price
    Common.plog_info("Sell list:")
    Common.plog_info(sell_list)



