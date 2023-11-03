import alpaca_trade_api as tradeapi

api_key = "CK397E5BUD1QAYWUMAJL"

api_secret = "CK0CO33HX6QU63TWCXJ2"


api = tradeapi.REST(api_key, api_secret)
account = api.get_account()
api.list_positions()