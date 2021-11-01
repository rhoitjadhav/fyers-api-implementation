import sys
sys.path.insert(0, "/home/piyush/Documents/fyers_v2/Python_SDK/fyers-api-py/")
from fyers_api import fyersModel
import webbrowser
from fyers_api import accessToken
from fyers_api.Websocket import ws
import time
# import asyncio

def api_call(token,client_id):
	# access_token = "your_access_token_from_generate_access_token_function" ## access_token from the rgenerate_access_token function
	## If you want to make asynchronous API calls then assign the below variable as True and then pass it in the functions, by default its value is False
	# is_async = True
	access_token = token
	# appId = client_id.split(":")[0]
	# import ipdb;ipdb.set_trace()
	fyers = fyersModel.FyersModel(token=access_token,is_async=True,client_id=client_id)
	fyers.token = access_token
	#
	# print(fyers.get_profile())
	# data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"0","range_from":"1622097600","range_to":"1622097685","cont_flag":"1"}
	# print(fyers.history(data))
	# start_time = time.time()
	# print(fyers.quotes({"symbols":"NSE:ONGC-EQ,NSE:SBIN-EQ"}))
	# end_time = time.time()
	# print(f"end_time:{end_time-start_time}")
	# print(fyers.depth({"symbol":"NSE:SBIN-EQ","ohlcv_flag":"0"}))
	# print(fyers.ws.({"data_type":"symbolUpdate","symbol":"MCX:SILVERMIC21JUNFUT"}))
	# print(fyers.tradebook())
	# print(fyers.tradebook_with_filter({"orderNumber":"808078094451"}))  #tradebook_with_filter
	# print(fyers.positions())
	# print(fyers.holdings())
	# print(fyers.holdings_with_filter({"symbol":"NSE:JPASSOCIAT-"}))
	# print(fyers.convert_position({"symbol":"MCX:SILVERMIC20AUGFUT","positionSide":"1","convertQty":"1","convertFrom":"MARGIN","convertTo":"INTRADAY"}))
	# print(fyers.funds())
	# print(fyers.funds_with_filter({'id':"1"}))
	# print(fyers.orderBook())
	# print(fyers.orderBook_with_filter({'id':'808078094451'}))
	# print(fyers.cancel_orders({'id':'8080582117761'}))
	# print(fyers.place_orders({"symbol":"MCX:SILVERMIC20AUGFUT","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"76700","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"}))
	# print(fyers.modify_orders({"id":"808058117761", "qty":"0","type":"1","limitPrice":"71100","stopPrice":"0"})) #modify instead of update
	# # print(fyers.minquantity())
	# print(fyers.orderStatus_with_filter({'id':'808078094451'}))
	# # print(fyers.market_status())
	# print(fyers.exit_positions({"id":"MCX:SILVERMIC20AUGFUT-MARGIN"}))
	# # print(fyers.generate_data_token({"vendorApp":"0KMS0EZVXI"}))
	# # print(fyers.multiple_orders())
	# print(fyers.multiple_cancel_orders([{"id":"120080780536"},{"id":"120080777069"}]))
	# print(fyers.multiple_place_orders([{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"},{"symbol":"NSE:SBIN-EQ","qty":"1","type":"1","side":"1","productType":"INTRADAY","limitPrice":"191","stopPrice":"0","disclosedQty":"0","validity":"DAY","offlineOrder":"False","stopLoss":"0","takeProfit":"0"}]))
	#
	# print(fyers.multiple_modify_orders([{"id":"120080780536", "type":1, "limitPrice": 190, "stopPrice":0},{"id":"120080777069", "type":1, "limitPrice": 190}]))
	
	# p = threading.Thread(target=fyersSocket.subscribe)
	# p.start()
	# data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"0","range_from":"1622097600","range_to":"1622097685","cont_flag":"1"}
	# fyers.history(data)
	# print(response)
	# for i in range(0,100):
	# 	print(fyers.get_profile())
	# 	print(fyers.tradebook())
	# 	print(fyers.positions())
	access_token = "L9NY34Z6BW-100:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MzM2Njc5MjksImV4cCI6MTYzMzczOTQ0OSwibmJmIjoxNjMzNjY3OTI5LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaFg4dFotcFZpOGdvYmMtMlRfNmNmYlowQlVFbVJFel9XSjJCRmJTRURWUm1GbDRzdW5tQ3FmQWN6bDVESkZsMEJLeEw3N3E5RUttMWRYNzcta05VaXhiNE4xY3ZoVGU0RGx4YUFBTERuekhqeU4xQT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.SqubA2d3axSDQW3xah8d_ZI_xFQSkDeSExv4EvotuGs"
	# # loop = asyncio.new_event_loop()
	data_type = "symbolData"
	# data_type = "orderUpdate"
	# symbol =  ["MCX:SILVERMIC21NOVFUT","MCX:NATURALGAS21SEPFUT"]
	symbol =["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX","NSE:NIFTYAUTO-INDEX","NSE:NIFTYALPHA50-INDEX","BSE:150MIDCAP-INDEX"]
	# symbol =["NSE:NIFTY50-INDEX"]
	# symbol=["NSE:NIFTY2190917350CE","NSE:NIFTY2190917350PE"]
	# symbol = ["NSE:SBIN-EQ","NSE:ONGC-EQ"]
		# fs = ws.FyersSocket(access_token=access_token, data_type=data_type,run_background=True)
	fs = ws.FyersSocket(access_token=access_token,run_background=False,log_path="/home/piyush/Downloads/")
	fs.websocket_data = custom_message
	# fs.on_open = onopen
	# fs.on_error = onerror
	# fs.init_connection()
	# time.sleep(5)
	# import ipdb;ipdb.set_trace()
	# fs.subscribe(symbol=symbol)
	# def op_open(fs,fetch_symbol):
	# 	on_open(fetch_data_symbolhigh low)
	# def on_close(fs,time):
	# 	on_close(3:15)
	# def custom_message(message):
	# 	message
	# fs.on_open()
	# fs.on_close()
	# fs.on_message()
	# fs.on_error()
	# fs.init_connection()
	# import ipdb;ipdb.set_trace()
	fs.subscribe(symbol=symbol,data_type=data_type)
	# # time.sleep(5)
	# # fs.subscribe(symbol=["MCX:SILVER21SEPFUT"])
	# print(fyers.get_profile())
	# print(fyers.tradebook())
	# print(fyers.positions())
	# # print("unsubscribed symbol")
	# # symbol = ["NSE:ONGC-EQ"]
	# # fs.unsubscribe(symbol=symbol)
	fs.keep_running()
	# fs.subscribe(run_background=False)
	# with ThreadPoolExecutor(3) as executor:
	# 	task = executor.submit(fs.subscribe())

def getauthToken(client_id,redirect_uri,response_type,scope,state,nonce):
	"""
		The variable `generateTokenUrl` will have a url like
		https://uat-api.fyers.in/api/dev/generate-authcode?appId=B8PWLVH8T6&redirectUrl=https%3A%2F%2Fgoogle.com
		 1. This function open this url in the browser.
		 2. This will ask you to login and will ask you to approve the app if it is not approved already.
		 3. Once that is done, it will redirect to a url (added while app creation) with the auth_code. The url will look like
		    https://www.google.com/?auth_code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM1ODY2NzEsInN1YiI6ImF1dGhDb2RlIiwiYXBwX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXVpZCI6ImZhOGNhYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg&user_id=DP00404
		 4. You have to take the auth_code from the url and use that token in your generate_access_token function.
	"""
	appSession = accessToken.SessionModel(client_id = client_id, redirect_uri = redirect_uri,response_type=response_type,scope=scope,state=state,nonce=nonce)
	generateTokenUrl = appSession.generate_authcode()
	print((generateTokenUrl))
	webbrowser.open(generateTokenUrl,new=1)

def generate_access_token(auth_code,client_id,redirect_uri,secret_key,grant_type):
	"""
	:param auth_code: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTM1ODY2NzEsInN1YiI6ImF1dGhDb2RlIiwiYXBwX2lkIjoiQjhQV0xWSDhUNiIsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsImF1ZCI6WyJ4OjAiLCJ4OjEiLCJ4OjIiXSwidXVpZCI6ImZhOGNhYjE3ZWU4OTQzMGRhZjA1YWUxNDI2YWVkYzI4IiwiaXBBZGRyIjoiMjIzLjIzMy40Mi40NiIsImRpc3BsYXlfbmFtZSI6IkRQMDA0MDQiLCJpYXQiOjE1OTM1ODYzNzEsIm5iZiI6MTU5MzU4NjM3MX0.IMJHzQGHQgyXt_XN0AgDrMN1keR4qolFFKO6cyXTnTg"
	:param app_id: "B8PWLVH8T6"
	:param secret_key: "575XQDKGN0"
	:param redirect_url: "https://google.com"
	:return: access_token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTM1ODgzNzMsIm5iZiI6MTU5MzU4ODM3MywiZXhwIjoxNTkzNjQ5ODEzLCJpc3MiOiJhcGkuZnllcnMuaW4iLCJzdWIiOiJhY2Nlc3MiLCJhdWQiOiJ4OjAseDoxLHg6MiIsImF0X2hhc2giOiJnQUFBQUFCZV9EcVZIZExMMTAzTVpVN1NYSkZfR2p5R3hidzMtTVVhb0VEMGI0QUVvNjFsR24tREY2OFU5cXhuNzd0UXVoOVVJalYtNm9MVXhINVFfWE1WTEJfRXpROGV2clJmUzlNUXB0Y2J5c2ltN1drWllZTT0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQifQ.cAfrj2TxAyb8A_9DfiCb1hLIZg_mH-xvP3Ybnj3a4AE"

	1.this function takes the param and return the access_token
	2.the access_token created will be used further .(in fyersModel)]
	3. one can get the auth_code from the url generated by getauthToken function (from auth_code= ..... &user_Id=xxxxxx before &)
	"""
	# import ipdb;
	# ipdb.set_trace()
	appSession = accessToken.SessionModel(client_id = client_id,redirect_uri =redirect_uri,secret_key = secret_key,grant_type=grant_type)
	appSession.set_token(auth_code)
	access_token = appSession.generate_token()
	return access_token

def custom_message(msg):
    print (f"Custom:{msg}")   

def onopen():
	print("Websocket connected")

def onerror(msg):
	print(msg)	

def main():

	redirect_uri= "https://beta-rest.tradingview.com/trading/oauth-redirect/fyers/"
	client_id = "L9NY34Z6BW-100"
	# client_id = "TWQFQCS0Q4-101"
	secret_key = "WGKBQ43W2G"
	grant_type = "authorization_code"
	response_type = "code"
	state = "sample"
	nonce = "baka"
	scope = "openid"
	# getauthToken(client_id, redirect_uri,response_type,scope,state,nonce)
	auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2MjM3NDEwMzAsImV4cCI6MTYyMzc0MTMzMCwibmJmIjoxNjIzNzQxMDMwLCJhdWQiOiJbXCJ4OjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIiwgXCJkOjFcIiwgXCJkOjJcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJEUDAwNDA0Iiwibm9uY2UiOiJiYWthIiwiYXBwX2lkIjoiR01FN0lBTFNZSiIsInV1aWQiOiJmMTJlMTEyZmQ5ODA0MWE2OWI0OGRiMDI5ZTIzOTdmNyIsImlwQWRkciI6IjY1LjEuMjU0LjI1MSIsInNjb3BlIjoib3BlbmlkIn0.0p_4K_D4CnNO3WCK49ZWq11Ho3mR1vYnPaX9u--AbAE"

	# print(generate_access_token(auth_code, client_id, redirect_uri,secret_key,grant_type))

	access_token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MzM1ODE3MzEsImV4cCI6MTYzMzY1MzAxMSwibmJmIjoxNjMzNTgxNzMxLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCaFhucWpFNjhncHMtNjRzZGxjc0lMNFl0UmktQWRNeGdhcjByREs2RVlTbXVxQ0puVm0zWjN4Vk1hLXBsbV9GQzl1c0lwT3liUHVySGI4eURTUGZwTWdRNkVXNzZmNzFxS1JmWTcyUkZrWXZLX3AzZz0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.U3qRPL3kJrE9gZq6DvPX14pHK3yikd826q25hhwOWpg"

	api_call(access_token , client_id)

if __name__ == '__main__':
	main()

