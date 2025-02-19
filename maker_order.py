
# key api test2
import sys
import time, math
from binance_ft.um_futures import UMFutures
from helper import get_commision, get_precision, get_status_pos, key, secret
import argparse

parser = argparse.ArgumentParser(description='A simple example script to demonstrate argparse')
parser.add_argument('pair', type=str, default= "ORDIUSDC",help='The name of the pair to process')
parser.add_argument("--vol", type=int, default=300)
parser.add_argument("--low", type=float, default=0.99)

parser.add_argument("--s", action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    um_futures_client = UMFutures(key=key, secret=secret)

    # um_futures_client = UMFutures(key="c21f1bb909318f36de0f915077deadac8322ad7df00c93606970441674c1b39b", secret="be2d7e74239b2e959b3446b880451cbb4dee2e6be9d391c4c55ae7ca0976f403", base_url="https://testnet.binancefuture.com")

    usdt = args.vol


    pair = args.pair
    print("******", pair, "*******")

    precision_ft = get_precision(pair, um_futures_client)


    # now_ft_price = float(um_futures_client.mark_price(pair)['markPrice']) 
    # bid_price = float(um_futures_client.book_ticker(pair)['bidPrice'])
    askPrice = float(um_futures_client.book_ticker(pair)['askPrice'])



    quantity_ft = round((usdt)/askPrice, precision_ft)
    print("askPrice:", round(askPrice,4), "quantity: ", quantity_ft)

    a,b,c  = get_status_pos(pair, um_futures_client)
    if not args.s and c != 0:
        usdt_open = usdt
        commis = usdt * 0.0005
        coin_open = c
        mean_price = a
        all_pnl = b
        coin_open = round(coin_open, precision_ft)
        print(f"already set a open at {a}, with {coin_open} {pair}, pnl {b}")
    else:
        open_future = um_futures_client.new_order(symbol=pair, side="SELL", type="LIMIT", quantity=quantity_ft, price = askPrice, timeInForce="GTC")
        # open_future = um_futures_client.new_order(symbol=pair, side="SELL", type="MARKET", quantity=quantity_ft)        
        commis, usdt_open, coin_open, mean_price, all_pnl = get_commision(open_future['orderId'], um_futures_client, pair)
        coin_open = round(coin_open, precision_ft)

    low_ratio = args.low
    high_ratio = 1.05

    


    print(f"commis: {commis:.3f}, usdt_open: {usdt_open:.3f} coin_open: {coin_open:.3f}, mean_price: {mean_price:.3f}")
    print("[SELL] close if price lower: ", mean_price * low_ratio, "or higher than", mean_price * high_ratio)
    while True:
        ask_price = float(um_futures_client.book_ticker(pair)['askPrice'])
        if ask_price < mean_price *low_ratio or ask_price > mean_price * high_ratio:
            print("ask_price", ask_price)
            close_future = um_futures_client.new_order(symbol=pair, side="BUY", type="MARKET", quantity=coin_open)
            time.sleep(1)
            break
        time.sleep(0.1)

    commision_close, all_spend_close, all_coin_close, mean_price_close, all_pnl_close = get_commision(close_future['orderId'], um_futures_client, pair)

    column_width = 20
    print(f"commision_close: {commision_close:.3f}, usdt_close: {all_spend_close:.3f} coin_close: {all_coin_close:.3f}, mean_price_close: {mean_price_close:.3f}, ")

    print("final pnl: ", all_pnl_close - commis - commision_close)



