import mock

__author__ = 'eugenel'
import unittest
from mock import patch, Mock, MagicMock
import quoteRest
import Common
import config
import level2

class level2Test(unittest.TestCase):

    @mock.patch('quoteRest.set_order')
    @mock.patch('Common.price_loop')
    def test_buy_shares_negative(self, mock_price_loop, mock_set_order):
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