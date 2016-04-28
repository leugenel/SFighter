__author__ = 'eugenel'
import time
import config
import sys
import Common
import quoteRest
import logging


logging.basicConfig(filename='level2.log',level=logging.DEBUG, filemode='w')
sleep_time = 0.1  # sec
num_iterations = 10
number_bids = 10
num_shares = 10
all_profit=0
all_buy=0
all_sell=0
#sell_list = {}

def buy_shares(buy_this_value):
    buy_done = False
    # Try buy 400 shares
    the_price = Common.price_loop(sleep_time, num_iterations)
    response, result = quoteRest.set_order(config.venue, config.stock, config.account, the_price, buy_this_value,
                                           "buy", "fill-or-kill")
    Common.plog_info("Buy result:")
    Common.plog_info(result)
    if response != 200:
        Common.plog_info(response)
        sys.exit()
    if result['totalFilled'] > 0:
        buy_done=True
        Common.plog_info("Set order for buy:")

    # Verify that buying works
    # for i in range (1, num_iterations):
    #     if quoteRest.get_order_status(config.venue, config.stock, result['id']):
    #         buy_done=True
    #         break
    #     time.sleep(sleep_time)
    # # Cancel order if not buy it
    # if not buy_done:
    #     quoteRest.cancel_order(config.venue, config.stock, result['id'])
    #     Common.plog_info("Cancel buy order")



    return buy_done, the_price, result['id']

def sell_shares(sell_this_value, price, update_price, price_delta):
    sell_done = False
    #update_price = 100
    #price_delta = 10
    sell_price = 0
    num_selled = 0
    for j in range (1, num_iterations):
        update_price -= price_delta
        response, result_json = quoteRest.set_order(config.venue, config.stock, config.account, price+update_price, sell_this_value, "sell")
        if response != 200:
            Common.plog_info(response)
            sys.exit()
        sell_id = result_json['id']
        Common.plog_info("Set order for sell:")
        Common.plog_info(result_json)
        is_ok, result_json = quoteRest.get_order_status(config.venue, config.stock, sell_id)
        num_selled = int (result_json['totalFilled'])
        Common.plog_info("Status of the selling order "+str(result_json))
        if is_ok:
            sell_done = True
            sell_price += int(result_json['price'])
            Common.plog_info("Sell done for price "+str(sell_price))
            break
        else:
            if num_selled > 0:
                Common.plog_info("We sell "+result_json['totalFilled']+ "shares")
                sell_this_value-= num_selled
                if(sell_this_value<=0):
                    Common.plog_info("sell_this value is " + str(sell_this_value))
                    break
                sell_price = int(result_json['price'])
            quoteRest.cancel_order(config.venue, config.stock, sell_id)
        time.sleep(sleep_time)
    if not sell_done:
        Common.plog_info("Not sell this package")
    return sell_done, sell_price, num_selled

is_sel = True
mcount=0
while mcount<10:
    # Try buy  shares
    price_buy = 0
    if is_sel:
        is_buy, price_buy, share_id = buy_shares(num_shares)
        if not is_buy:
            Common.plog_info("Not success to buy this package")
            continue
        all_buy+=price_buy
        Common.plog_info("Now buy :"+str(price_buy))
        Common.plog_info("Summary buy: ")
        Common.plog_info(all_buy)
        all_profit-=all_buy

    #Now selling
    if price_buy > 0:
        is_sel, sell_price, num_selled = sell_shares(num_shares, price_buy, 100, 10)
        if is_sel:
            all_sell+=sell_price
            Common.plog_info("Summary sell: ")
            Common.plog_info(all_sell)
            mcount+=1
        else:
            is_sel=False
            Common.plog_info("No sell done")
            is_sel, sell_price, num_selled = sell_shares(num_shares, price_buy, 0, 0)
    else:
        Common.plog_info("Price for selling is 0")
        sys.exit()
    all_profit+=all_sell
    Common.plog_info("Current profit: "+str(all_profit))