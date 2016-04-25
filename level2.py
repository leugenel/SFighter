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
all_profit=0
all_buy=0
all_sell=0
#sell_list = {}

def buy_shares(buy_this_value):
    buy_done = False
    # Try buy 400 shares
    the_price = Common.price_loop(sleep_time, num_iterations)
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, the_price, buy_this_value)
    if response != 200:
        Common.plog_info(response)
        sys.exit()
    Common.plog_info("Set order for buy:")
    Common.plog_info(result)
    # Verify that buying works
    for i in range (1, num_iterations):
        if quoteRest.get_order_status(config.venue, config.stock, result['id']):
            buy_done=True
            break
        time.sleep(sleep_time)
    # Cancel order if not buy it
    if not buy_done:
        quoteRest.cancel_order(config.venue, config.stock, result['id'])
        Common.plog_info("Cancel buy order")

    return buy_done, the_price, result['id']

def sell_shares(sell_this_value, price):
    sell_done = False
    update_price = 100
    price_delta = 10
    for j in range (1, num_iterations):
        update_price -= price_delta
        response, result = quoteRest.set_order(config.venue, config.stock, config.account, price+update_price, sell_this_value, "sell")
        if response != 200:
            Common.plog_info(response)
            sys.exit()
        Common.plog_info("Set order for sell:")
        Common.plog_info(result)
        if quoteRest.get_order_status(config.venue, config.stock, share_id):
            sell_done = True
            Common.plog_info("Sell done for price "+str(price+update_price))
            break
        time.sleep(sleep_time)
    if not sell_done:
        Common.plog_info("Not sell this package")
        #sell_list[share_id]=price+update_price
    #Common.plog_info("Sell list:")
    #Common.plog_info(sell_list)

    return sell_done, price+update_price

is_sel = True
while True:
    # Try buy 400 shares
    price_buy = 0
    if is_sel:
        is_buy, price_buy, share_id = buy_shares(num_shares)
        if not is_buy:
            Common.plog_info("Not success to buy this package")
            continue
        all_buy+=price_buy
        Common.plog_info(all_buy)
        all_profit-=all_buy

    #Now selling
    if price_buy > 0:
        is_sel, sell_price = sell_shares(num_shares, price_buy)
        all_sell+=sell_price
        Common.plog_info(all_sell)
    else:
        Common.plog_info("Price for buying is 0")
    all_profit+=all_sell
    Common.plog_info("Current profit: "+str(all_profit))