moduleName = "accessToken"
try:
	from .fyersService import FyersService
	import json
	from .config import Config
	import urllib
	import hashlib
except Exception as e:
	print("moduleName: {}, ERR: {}".format(moduleName, e))


class SessionModel:
	def __init__(self,client_id = None,redirect_uri = None,response_type=None,scope=None,state=None,nonce=None,secret_key = None,grant_type=None):
		self.client_id = client_id
		self.redirect_uri = redirect_uri
		self.response_type = response_type
		self.scope = scope
		self.state = state
		self.nonce = nonce
		self.secret_key = secret_key
		self.grant_type = grant_type

	def generate_authcode(self):
		data = {"client_id":self.client_id, "redirect_uri":self.redirect_uri,"response_type":self.response_type,"state":self.state}
		
		if self.scope is not None:
			data["scope"] = self.scope

		if self.nonce is not None:
			data["nonce"] = self.nonce
		
		url = Config.Api + Config.auth
		if data is not None:
			try:
				url_params = urllib.urlencode(data)
			except Exception as e:
				url_params = urllib.parse.urlencode(data)
			response = url + "?" + url_params
		return response

	def get_hash(self):
		hash_val= result = hashlib.sha256((self.client_id+":"+self.secret_key).encode())
		return hash_val

	def set_token(self,token):
		self.auth_token = token
		return True

	def generate_token(self):
		data = {"grant_type":self.grant_type,"appIdHash":(self.get_hash()).hexdigest(),"code":self.auth_token}
		service = FyersService()
		response = service.postCall(Config.generateAccessToken,"",data)
		return response