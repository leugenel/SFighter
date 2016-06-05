__author__ = 'eugenel'
import time
import config
import sys
import Common
import quoteRest
import logging
import threading

class SellSide(object):
    SLEEP_TIME = 0.1
    NUM_ITERATIONS = 10
    NUM_SHARES = 30
    UPDATE_PRICE = 100
    DELTA_PRICE = 10

    qty_filled_buy = 0
    buy_price = 0

    all_profit=0
    all_buy=0
    all_sell=0

    def __init__(self):
        logging.basicConfig(filename='level2.log',level=logging.DEBUG, filemode='w',
                            format='[%(levelname)s] (%(threadName)-10s) %(message)s')

    """
        Main threads procedure
    """
    def start_all(self, num_threads):
        threads = [ ]
        for i in range(num_threads):
            thread = threading.Thread(target=self.game_run)
            threads.append(thread)
            thread.start()

    """
        Main one thread procedure
    """
    def game_run(self):
        for i in range (1, self.NUM_ITERATIONS*10):
            if not self.buy_shares(self.NUM_SHARES):
                continue
            self.sell_shares(self.NUM_SHARES)

    """
        Responsible for buy share, doing in the fill-or-kill mode means delete order if not buy.
        Not need to cancel the order because the mode
    """
    def buy_shares(self, buy_this_value):
        the_price = Common.price_loop(self.SLEEP_TIME, self.NUM_ITERATIONS)
        Common.plog_info("The buy price from price_loop:" + str(the_price))
        response, result = quoteRest.set_order(config.venue, config.stock, config.account, the_price, buy_this_value,
                                               "buy", "fill-or-kill")
        Common.plog_info("Buying...")
        self.response_process(response, result)
        self.qty_filled_buy = result['totalFilled']
        if self.qty_filled_buy > 0:
            self.buy_price = result['price']
            self.all_buy += self.buy_price
            self.all_profit -= self.buy_price
            Common.plog_info("===============================================================")
            Common.plog_info("We buy :"+str(self.buy_price)+" The all buy until now: "+
                             str(self.all_buy)+" Tha all profit: "+str(self.all_profit))
            Common.plog_info("===============================================================")
        else:
            Common.plog_info("Not success to buy this package. Built the new one")
            return False

        return True

    """
        Three loops try to sell the order, first for the profit, second for the same price, third lost the money
        We hope this enough to sell
    """
    def sell_shares(self, sell_this_value):
        order_sell = sell_this_value
        Common.plog_info("Try sell with profit")
        qty_filled_sell, sell_price = self.sell_loop(self.buy_price + self.UPDATE_PRICE, order_sell, self.DELTA_PRICE)
        if qty_filled_sell < sell_this_value:  # Now we sell for the original price - no profit
            Common.plog_info("Try sell w/o profit")
            qty_filled_sell_t, sell_price_t = self.sell_loop(self.buy_price, sell_this_value-qty_filled_sell)  # no delta we sell in constant price
            qty_filled_sell += qty_filled_sell_t
            sell_price += sell_price_t
        if qty_filled_sell < sell_this_value: # Now we sell for the worse price - lost money
            Common.plog_info("Try sell with lost money")  # with delta we decrease the price
            qty_filled_sell_t, sell_price_t = self.sell_loop(self.buy_price, sell_this_value-qty_filled_sell, self.DELTA_PRICE)
            qty_filled_sell += qty_filled_sell_t
            sell_price += sell_price_t

        self.all_sell += qty_filled_sell
        self.all_profit += sell_price
        Common.plog_info("===============================================================")
        Common.plog_info("We sell number of shares: "+str(qty_filled_sell)+ " We sell $: "+ str(sell_price)+
                         " All sell until now: "+str(self.all_sell)+" All profit: "+str(self.all_profit))
        Common.plog_info("===============================================================")

    """
        Minimal sell loop.
        Decrease the price each iteration until the original price.
        Return how much we sold
    """
    def sell_loop(self, price, num_to_sell, delta_price=0):
        if num_to_sell <= 0:
            Common.plog_info("Nothing to sell")
            return 0, 0
        sell_now = num_to_sell
        how_much_we_sold = 0
        sold_price = 0
        for i in range (1, self.NUM_ITERATIONS):
            sold, sold_price = self.basic_sell(sell_now, price-delta_price*i)
            how_much_we_sold+=sold
            if sold == sell_now:
                Common.plog_info("We sell everything in this set")
                break
            sell_now -= sold
            if sell_now < 0:
                raise ValueError("Sell can't be negative")
            Common.plog_info("We continue sell "+str(sell_now))

        return how_much_we_sold, sold_price

    """
        Basic sell
        One sell tact with the price.
        After timeout if not sailed cancel the request.
    """
    def basic_sell(self, sell_this_value, price):
        response, result_json = quoteRest.set_order(config.venue, config.stock, config.account,
                                                    price,
                                                    sell_this_value, "sell")
        Common.plog_info("Selling...")
        self.response_process(response, result_json)
        sell_id = result_json['id']
        time.sleep(self.SLEEP_TIME)
        quoteRest.cancel_order(config.venue, config.stock, sell_id)
        is_ok, result_json_status = quoteRest.get_order_status(config.venue, config.stock, sell_id)
        Common.plog_info("Sell status:")
        self.response_process(response, result_json_status)
        return result_json_status['totalFilled'], result_json_status['price']

    """
            Response processing
    """
    def response_process(self, response, result):
        if response != 200:
            Common.plog_info("We failed with " + str(response))
            sys.exit()
        Common.plog_info("The result: "+str(result))


if __name__ == '__main__':
    SellSide().start_all(2)

