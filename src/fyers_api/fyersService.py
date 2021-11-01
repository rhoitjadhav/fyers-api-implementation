moduleName = "fyersService"

try:
    from .config import Config
    import requests
    import json
    import urllib
    from .fyersFormation import FyersFormation
    from tornado import httpclient
    from datetime import datetime, timezone

except Exception as e:
    print("moduleName: {}, ERR: {}".format(moduleName, e))

formService = FyersFormation()

class FyersService:

    def __init__(self,logObj= None):
        self.logObj = logObj
        self.content = 'application/json'

    def postCall(self, api, header, data=None):
        try:
            response = requests.post(Config.Api + api, headers={"Authorization": header, 'Content-Type':self.content}, json=data)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "","", e)
        if type(response)==dict:
            return response
        return response.json()

    def getCall(self, api, header, data=None,data_flag=False):
        try:
            if data_flag:
                url = Config.data_Api + api
            else:
                url = Config.Api + api
            if data is not None:
                try:
                    url_params = urllib.urlencode(data)
                except Exception as e:
                    url_params = urllib.parse.urlencode(data)
                url = url + "?" + url_params
            response = requests.get(url=url, headers={"Authorization": header, 'Content-Type': self.content})
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        return response.json()

    def deleteCall(self, api, header, data):
        try:
            response = requests.delete(url=Config.Api + api,headers={"Authorization": header, 'Content-Type': self.content}, json=data)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        if type(response)==dict:
            return response
        return response.json()

    def putCall(self, api, header, data):
        try:
            response = requests.put(url=Config.Api + api,headers={"Authorization": header, 'Content-Type': self.content}, json=data)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        if type(response)==dict:
            return response
        return response.json()


class FyersAsyncService:

    def __init__(self,logObj=None):
        self.logObj = logObj
        self.content = 'application/json'

    def postCall(self, api, header, data=None):
        try:
            reqClient = httpclient.AsyncHTTPClient()
            request = httpclient.HTTPRequest(Config.Api + api, method="POST", body=json.dumps(data),headers={"Authorization": header, 'Content-Type': self.content})
            response = reqClient.fetch(request, raise_error=False)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        return response

    def getCall(self, api, header, data=None,data_flag=False):
        try:
            if data_flag:
                url = Config.data_Api + api
            else:
                url = Config.Api + api
            reqClient = httpclient.AsyncHTTPClient()
            if data is not None:
                try:
                    url_params = urllib.urlencode(data)
                except Exception as e:
                    url_params = urllib.parse.urlencode(data)
                url = url + "?" + url_params
                request = httpclient.HTTPRequest(url, method="GET",headers={"Authorization": header, 'Content-Type': self.content})
            else:
                URL = url
                request = httpclient.HTTPRequest(URL, method="GET",headers={"Authorization": header, 'Content-Type': self.content})

            response = reqClient.fetch(request, raise_error=False)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        return response

    def deleteCall(self, api, header, data):
        try:
            reqClient = httpclient.AsyncHTTPClient()
            request = httpclient.HTTPRequest(Config.Api + api, method="DELETE", body=json.dumps(data),headers={"Authorization": header, 'Content-Type': self.content},allow_nonstandard_methods=True)
            response = reqClient.fetch(request, raise_error=False)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        return response

    def putCall(self, api, header, data):
        try:
            reqClient = httpclient.AsyncHTTPClient()
            request = httpclient.HTTPRequest(Config.Api + api, method="PUT", body=json.dumps(data),headers={"Authorization": header, 'Content-Type': self.content})
            response = reqClient.fetch(request, raise_error=False)
        except Exception as e:
            response = formService.exceptionRaised(e)
            if self.logObj is not None:
                self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "getCall", "", "",e)
        return response