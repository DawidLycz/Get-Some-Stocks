from unittest.mock import patch
from pandas.testing import assert_frame_equal
import pandas as pd
from django.test import TestCase
from getstocksapp.models import Market, Ticker
from .data_downloaders.yfinance_data import get_stock_data


class TickerModelTest(TestCase):
    @patch("getstocksapp.data_downloaders.yfinance_data.yf.download")
    def test_get_stock_data(self, mock_download):
        fake_data = {
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Open": [100.0, 105.0, 98.0],
            "High": [110.0, 112.0, 100.0],
            "Low": [95.0, 100.0, 94.0],
            "Close": [105.0, 102.0, 96.0],
            "Volume": [1000000, 1200000, 800000],
        }
        with patch("getstocksapp.data_downloaders.yfinance_data.get_stock_data") as mock_data:

            mock_download.return_value = pd.DataFrame(fake_data)
            
            result = get_stock_data(ticker="AAPL")

            expected_data = pd.DataFrame(fake_data)
            expected_data = expected_data[::-1] 
            print (result)
            print (expected_data)


            self.assertTrue(result.equals(expected_data))
