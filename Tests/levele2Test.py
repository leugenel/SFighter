__author__ = 'eugenel'
import mock
import unittest
import quoteRest
import Common
import config
import level2

class level2Test(unittest.TestCase):

    @mock.patch('quoteRest.set_order')
    @mock.patch('Common.price_loop')
    def test_buy_shares_negative(self, mock_price_loop, mock_set_order):
        print "============================="
        print "Test test_buy_shares_negative"
        print "============================="
        # No fills in the result
        mock_result={u'direction': u'buy', u'ok': True, u'ts': u'2016-05-01T16:12:58.628599993Z',
                     u'fills': [], u'originalQty': 10, u'orderType': u'fill-or-kill',
                     u'symbol': u'FOOBAR', u'venue': u'TESTEX', u'account': u'EXB123456',
                     u'qty': 10, u'id': 1301, u'totalFilled': 0, u'open': False, u'price': 100}

        assert  mock_price_loop is Common.price_loop
        assert  mock_set_order is quoteRest.set_order

        sell = level2.SellSide()

        mock_set_order.return_value = (200, mock_result)
        mock_price_loop.return_value = 100

        sell.buy_shares(mock_result['qty'])

        mock_set_order.assert_called_with(config.venue, config.stock, config.account, 100, mock_result['qty'],
                                          "buy", "fill-or-kill")
        mock_price_loop.assert_called_with(sell.SLEEP_TIME, sell.NUM_ITERATIONS)

        assert sell.qty_filled_buy == 0
        assert sell.buy_price == 0
        assert sell.all_buy == 0
        assert sell.all_profit == 0

    @mock.patch('quoteRest.set_order')
    @mock.patch('Common.price_loop')
    def test_buy_shares(self, mock_price_loop, mock_set_order):
        print "============================="
        print "Test test_buy_shares"
        print "============================="
        mock_result = {u'direction': u'buy', u'ok': True, u'ts': u'2016-05-06T16:30:32.370347066Z',
                       u'fills': [{u'price': 8234, u'ts': u'2016-05-06T16:30:32.370349746Z', u'qty': 30}],
                       u'originalQty': 30, u'orderType': u'fill-or-kill', u'symbol': u'SOZO',
                       u'venue': u'CFMBEX', u'account': u'TDS46443102', u'qty': 0, u'id': 7413,
                       u'totalFilled': 30, u'open': False, u'price': 8234}

        assert  mock_price_loop is Common.price_loop
        assert  mock_set_order is quoteRest.set_order

        sell = level2.SellSide()

        mock_set_order.return_value = (200, mock_result)
        mock_price_loop.return_value = 100

        sell.buy_shares(mock_result['qty'])

        mock_set_order.assert_called_with(config.venue, config.stock, config.account, 100, mock_result['qty'],
                                          "buy", "fill-or-kill")
        mock_price_loop.assert_called_with(sell.SLEEP_TIME, sell.NUM_ITERATIONS)

        assert sell.qty_filled_buy == mock_result['totalFilled']
        assert sell.buy_price == mock_result['price']
        assert sell.all_buy == mock_result['price']
        assert sell.all_profit == - mock_result['price']

    @mock.patch('quoteRest.cancel_order')
    @mock.patch('quoteRest.set_order')
    @mock.patch('quoteRest.get_order_status')
    def test_basic_sell(self, mock_order_status, mock_set_order, mock_cancel_order):
        print "============================="
        print "Test test_basic_sell"
        print "============================="
        mock_result_set_order = {u'direction': u'sell', u'ok': True, u'ts': u'2016-05-06T16:30:33.345340136Z',
                                 u'fills': [], u'originalQty': 30, u'orderType': u'limit', u'symbol': u'SOZO',
                                 u'venue': u'CFMBEX', u'account': u'TDS46443102', u'qty': 30, u'id': 7414,
                                 u'totalFilled': 0, u'open': True, u'price': 8324}

        mock_result_order_status = {u'direction': u'sell', u'ok': True, u'ts': u'2016-05-06T16:31:00.888266762Z',
                                    u'fills': [{u'price': 8244, u'ts': u'2016-05-06T16:31:01.005217514Z', u'qty': 30}],
                                    u'originalQty': 30, u'orderType': u'limit', u'symbol': u'SOZO', u'venue': u'CFMBEX',
                                    u'account': u'TDS46443102', u'qty': 0, u'id': 7559, u'totalFilled': 30,
                                    u'open': False, u'price': 8244}

        assert  mock_set_order  is quoteRest.set_order
        assert  mock_order_status is quoteRest.get_order_status
        assert  mock_cancel_order is quoteRest.cancel_order

        sell = level2.SellSide()

        mock_set_order.return_value =  (200, mock_result_set_order)
        mock_cancel_order.return_value =  (200, None)
        mock_order_status.return_value = (200, mock_result_order_status)

        res, price = sell.basic_sell(30, 100)

        assert res == mock_result_order_status['totalFilled']
        assert price == mock_result_order_status['price']
#        assert sell.qty_filled_sell == mock_result_order_status['totalFilled'], "not equal:" + str(sell.qty_filled_sell) +\
#                                                                                " and "+ str(mock_result_order_status['totalFilled'])
#        assert sell.sell_price == mock_result_order_status['price']

    @mock.patch('quoteRest.cancel_order')
    @mock.patch('quoteRest.set_order')
    @mock.patch('quoteRest.get_order_status')
    def test_basic_sell_no_sell(self, mock_order_status, mock_set_order, mock_cancel_order):
        print "============================="
        print "Test test_basic_sell_no_sell"
        print "============================="
        mock_result_set_order = {u'direction': u'sell', u'ok': True, u'ts': u'2016-05-06T16:30:33.345340136Z',
                                 u'fills': [], u'originalQty': 30, u'orderType': u'limit', u'symbol': u'SOZO',
                                 u'venue': u'CFMBEX', u'account': u'TDS46443102', u'qty': 30, u'id': 7414,
                                 u'totalFilled': 0, u'open': True, u'price': 8324}

        mock_result_order_status = {u'direction': u'sell', u'ok': True, u'ts': u'2016-05-06T16:31:00.888266762Z',
                                    u'fills': [{u'price': 8244, u'ts': u'2016-05-06T16:31:01.005217514Z', u'qty': 30}],
                                    u'originalQty': 30, u'orderType': u'limit', u'symbol': u'SOZO', u'venue': u'CFMBEX',
                                    u'account': u'TDS46443102', u'qty': 0, u'id': 7559, u'totalFilled': 0,
                                    u'open': False, u'price': 0}

        assert  mock_set_order  is quoteRest.set_order
        assert  mock_order_status is quoteRest.get_order_status
        assert  mock_cancel_order is quoteRest.cancel_order

        sell = level2.SellSide()

        mock_set_order.return_value =  (200, mock_result_set_order)
        mock_cancel_order.return_value =  (200, None)
        mock_order_status.return_value = (200, mock_result_order_status)

        res, price = sell.basic_sell(30, 100)

        assert res == 0
        assert price == 0
#        assert sell.qty_filled_sell == 0
#        assert sell.sell_price == 0

    @mock.patch('level2.SellSide.basic_sell')
    def test_sell_loop(self, mock_basic_sell):
        print "============================="
        print "Test test_basic_sell_loop"
        print "============================="

        need_sell = 10
        price = 100
        sell = level2.SellSide()
        mock_basic_sell.return_value = need_sell

        res = sell.sell_loop(price, need_sell, sell.DELTA_PRICE)

        mock_basic_sell.assert_called_with(need_sell, price-sell.DELTA_PRICE)
        assert res == need_sell , "not equal:" + str(res) + " and "+ str(need_sell)

    @mock.patch('level2.SellSide.basic_sell')
    def test_sell_loop_with_zero(self, mock_basic_sell):
        print "============================="
        print "Test test_sell_loop_with_zero"
        print "============================="

        need_sell = 0
        price = 100
        sell = level2.SellSide()
        mock_basic_sell.return_value = need_sell

        res = sell.sell_loop(price, need_sell, sell.DELTA_PRICE)
        mock_basic_sell.assert_not_called()
        assert res == 0


    @mock.patch('level2.SellSide.basic_sell')
    def test_sell_loop_partial(self, mock_basic_sell):
        print "============================="
        print "Test test_sell_loop_partial"
        print "============================="

        need_sell = 10
        price = 100
        sell = level2.SellSide()
        mock_basic_sell.return_value = need_sell//2

        res = sell.sell_loop(price, need_sell, sell.DELTA_PRICE)

        mock_basic_sell.assert_any_call(need_sell, price-sell.DELTA_PRICE)
        mock_basic_sell.assert_any_call(need_sell//2, price-sell.DELTA_PRICE*2)
        assert res == need_sell , "not equal:" + str(res) + " and "+ str(need_sell)

    @mock.patch('level2.SellSide.basic_sell')
    def test_sell_loop_partial_with_exception(self, mock_basic_sell):
        print "============================="
        print "Test test_sell_loop_partial_with_exception"
        print "============================="

        need_sell = 10
        price = 100
        sell = level2.SellSide()
        mock_basic_sell.return_value = need_sell+5
        # Exception because negative sailing
        self.assertRaises(ValueError, sell.sell_loop, price, need_sell, sell.DELTA_PRICE)

    @mock.patch('level2.SellSide.sell_loop')
    def test_sell_shares_happy(self, mock_sell_loop):
        print "============================="
        print "Test test_sell_shares_happy"
        print "============================="

        sell = level2.SellSide()
        sell_this = 100
        price = 0
        sell.qty_filled_sell = sell_this
        mock_sell_loop.return_value = sell_this, price
        sell.sell_shares(sell_this)
        assert sell.all_sell == sell_this, "not equal:" + str(sell.all_sell) + " and "+ str(sell_this)

