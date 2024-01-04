from unittest.mock import patch
from pandas.testing import assert_frame_equal
import pandas as pd
from django.test import TestCase
from getstocksapp.models import Market, Ticker
from .data_downloaders.yfinance_data import get_stock_data


class TestTickerModel(TestCase):
    @patch('getstocksapp.data_downloaders.yfinance_data.get_stock_data', return_value=pd.DataFrame({'Open': [100, 105], 'Close': [110, 115]}))
    def test_get_stock_data(self, mock_yfinance_download):
        
        print(mock_yfinance_download)
        fake_data = {
            "Date": ["2023-01-01", "2023-01-02", "2023-01-03"],
            "Open": [100.0, 105.0, 98.0],
            "High": [110.0, 112.0, 100.0],
            "Low": [95.0, 100.0, 94.0],
            "Close": [105.0, 102.0, 96.0],
            "Volume": [1000000, 1200000, 800000],
        }
        assert_frame_equal(get_stock_data(ticker="AAPL"), pd.DataFrame(fake_data))


# baker faker 
