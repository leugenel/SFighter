__author__ = 'eugenel'
import unittest
from mock import patch, Mock, MagicMock
import quoteRest
import httplib

class QuoteRestTest(unittest.TestCase):

    def test_happy(self):
        mock_result={u'lastTrade': u'2016-04-28T19:49:05.772834259Z', u'ok': True,
                     u'last': 10197, u'askSize': 55, u'symbol': u'RII', u'venue': u'MWTEX',
                     u'lastSize': 39, u'bidDepth': 1332, u'askDepth': 110, u'ask': 10097,
                     u'bidSize': 444, u'bid': 9997, u'quoteTime': u'2016-04-28T19:49:05.80591967Z'}
        mock_quote_quick = quoteRest
        mock_quote_quick.quote_quick = MagicMock(return_value=(200, mock_result))
        response, result = mock_quote_quick.quote_quick("bbb", mock_result)
        mock_quote_quick.quote_quick.assert_called_with("bbb", mock_result)
        assert response == 200 and result['ok']

    def test_resp400(self):
        mock_result=None
        mock_quote_quick = quoteRest
        mock_quote_quick.quote_quick = MagicMock(return_value=(400, mock_result))
        response, result = mock_quote_quick.quote_quick("bbb", mock_result)
        mock_quote_quick.quote_quick.assert_called_with("bbb", mock_result)
        assert response == 400 and (result is None)