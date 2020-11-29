import json, os
from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"), tld=('com'))

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return True

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/webhook', methods=['POST'])
def webhook():

    #print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != os.getenv("WEBHOOK_PASSPHRASE"):
        return{
            "code":"error",
            "message":"Nice Try!, invalid passphrase"
        }
    
    print('Sending Orders:', "from", data['exchange'], data['strategy']['order_action'].upper(), ">>",data['strategy']['order_contracts'], data['ticker'],"@" , data['strategy']['order_price'])
    
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker']

    order_response = order(side, quantity, symbol)
    print(order_response)

    if order_response:
        return{
            "code":"success",
            "message":"order executed"
        }
    else:
        print("order failed")

        return{
            "code":"error",
            "message":"order failed"
        }


    return {
        "code":"success",
        "message": data
    }