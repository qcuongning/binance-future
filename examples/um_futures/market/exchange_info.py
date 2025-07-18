#!/usr/bin/env python
import sys
sys.path.append(".")
import logging
from binance_ft.um_futures import UMFutures
from binance_ft.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

um_futures_client = UMFutures()
logging.info(um_futures_client.exchange_info())
