from unittest.mock import patch
from pandas.testing import assert_frame_equal
import pandas as pd
from django.test import TestCase
from getstocksapp.models import Market, Ticker
from .data_downloaders.yfinance_data import get_stock_data


# baker faker 
