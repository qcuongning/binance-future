#!/usr/bin/env python
import logging
from binance_ft.cm_futures import CMFutures
from binance_ft.lib.utils import config_logging

config_logging(logging, logging.DEBUG)

cm_futures_client = CMFutures()

logging.info(cm_futures_client.mark_price_klines("FTMUSD_PERP", "1d", **{"limit": 500}))
