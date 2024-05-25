from telethon import TelegramClient, events
from binance.client import Client
# from binance import AsyncClient
from binance.enums import *
from binance.helpers import round_step_size

import json
import asyncio
import re

async def foo_bar(side, pair_name, entry_price1, entry_price2, target_price1, target_price2, target_price3, stop_loss):
    print("Inside Binance Funtion \n")
    print("Buy/Sell: ",side,"\n")
    print("Pair Name: ",pair_name,"\n")
    print("Entry Price_1: ",entry_price1,"\n")
    print("Entry Price_2: ",entry_price2,"\n")
    print("Target Prices: ",target_price1," " ,target_price2," " ,target_price3,"\n")
    print("Stop Loss: ",stop_loss,"\n")
    
    api_key = ''
    api_secret = ''
    
    binance_client = Client(api_key, api_secret)
    
    symbol_info = binance_client.get_symbol_info(pair_name)
    stepsize = float(symbol_info['filters'][1]['stepSize'])*100
    
    try:
        binance_client.futures_change_leverage(symbol=pair_name,leverage=10)
        binance_client.futures_change_margin_type(symbol=pair_name, marginType = 'ISOLATED')
    except:
        print("Margin and Leverage already set to ISOLATED and 10x")
    
#     price = await binance_client.get_avg_price(symbol=pair_name)
#     price = float(price['price'])
    quantity = round_step_size((100/entry_price1),stepsize)

    
    print("Quantity: ", quantity)
    if side == "BUY":
        try:
            market_res = binance_client.futures_create_order(symbol = pair_name, side = side, type = 'LIMIT', quantity = quantity, price = entry_price1 , timeInForce = TIME_IN_FORCE_GTC)
            stop_loss_order = binance_client.futures_create_order(symbol = pair_name,side='SELL', type='STOP', stopPrice = stop_loss, quantity = quantity, price = stop_loss)
            take_profit_order = binance_client.futures_create_order(symbol = pair_name ,side = 'SELL', type='TAKE_PROFIT', stopPrice = target_price1, quantity = quantity, price = target_price1)   
        except Exception as e:
            print(e)
        else:
            print(json.dumps(market_res, indent=2))
    else:
        try:
            market_res = binance_client.futures_create_order(symbol = pair_name, side = side, type = 'LIMIT', quantity = quantity, price = entry_price1 , timeInForce = TIME_IN_FORCE_GTC)
            stop_loss_order = binance_client.futures_create_order(symbol = pair_name, side='BUY', type='STOP', stopPrice = stop_loss, quantity = quantity, price = stop_loss)
            take_profit_order = binance_client.futures_create_order(symbol = pair_name ,side = 'BUY', type='TAKE_PROFIT', stopPrice = target_price1, quantity = quantity, price = target_price1)
        except Exception as e:
            print(e)
        else:
            print(json.dumps(market_res, indent=2))    
     
    print("Closing Binance Connection")   
    binance_client.close_connection()


async def login():
    api_id =
    api_hash = ''

    # Use your own API_ID and API_HASH from https://my.telegram.org/apps
    client = TelegramClient('crypto1', api_id, api_hash)

    # Connect to Telegram
    await client.start()

    # Get the entity of the group you want to save messages from
    group_entity = await client.get_entity(-1001691636888)
    # -1001691636888


    # Handle new messages in the group
    # "(?i)" makes it case-insensitive, and | separates "options"
    @client.on(events.NewMessage(chats=group_entity))
    async def my_event_handler(event):
        # Save the message text to a file
        msg = event.raw_text
        for_type ="\([A-Za-z]+\)" 
        for_pair_name = "#[A-Za-z]+/[A-Za-z]+"
        for_entry_price = "0?[.]?[0-9]+[.0-9]+[\s\n]"
        
        
        pat1 = re.compile(for_pair_name)
        pat2 = re.compile(for_entry_price)
        pat3 = re.compile(for_type)
        
        try:            
            side = ""
            buy_sell = re.findall(pat3,msg)[0][1:-1].strip()
            if buy_sell == "LONG":
                side = "BUY"
            else:
                side = "SELL"
            
            str1 = re.findall(pat1, msg)[0].strip()[1:]
            pair_name = str1[:-5]+str1[-4:].upper()
            
            entry_price1 = float(re.findall(pat2,msg)[0].strip())
            entry_price2 = float(re.findall(pat2,msg)[1].strip())
            
            target_price1 = float(re.findall(pat2,msg)[2].strip())
            target_price2 = float(re.findall(pat2,msg)[3].strip())
            target_price3 = float(re.findall(pat2,msg)[4].strip())
            
            stop_loss = float(re.findall(pat2,msg)[-1][:-1])
            
            await foo_bar(side,pair_name,entry_price1,entry_price2,target_price1,target_price2,target_price3,stop_loss)
        except:
            print("Exception Occured. Continuing...")
        
    # Start listening for new messages
    # client.add_event_handler(my_event_handler)
    try:
        print('(Press Ctrl+C to stop this)')
        await client.run_until_disconnected()
    finally:
        await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(login())