#from .woqlClient import (errorMessage)
import errorMessage
import const
import requests

from utils import Utils

from base64 import b64encode

class DispatchRequest:

	def __init__(self):
		pass
		#header= {'user-agent': 'my-app/0.0.1'}
#json.dumps

	def getCall(self,url,payload):
		headers=self._autorizationHeader(payload)
		params={}

		url=Utils.addParamsToUrl(url,payload)

		return requests.get(url,headers=headers)

	def postCall(self,options,payload,url):
		headers=self._autorizationHeader(payload);
		headers['content-type']= 'application/json'
		return requests.post(url,json=payload,headers=headers);

	def deleteCall(self,url):
		url=Utils.addParamsToUrl(url,payload)
		headers=self._autorizationHeader(payload);
		return requests.delete(url,headers=headers);

	def _autorizationHeader(self,payload):
		headers={}

		if (payload and ('terminus:user_key' in  payload)):
			headers = { 'Authorization: Basic %s' % b64encode(payload['terminus:user_key']).encode('utf-8')}#Utils.encodeURIComponent(payload['terminus:user_key'])}
			payload.pop('terminus:user_key')
		return headers

	def sendRequestByAction(self, url, action, payload):
		print("sendRequestByAction")
		try:
			requestResponse=None
			if (action == const.CONNECT 
				or action==const.GET_SCHEMA 
				or action==const.CLASS_FRAME 
				or action==const.WOQL_SELECT 
				or action==const.GET_DOCUMENT):
				requestResponse= self.getCall(url,payload)
			
			elif(action==const.DELETE_DATABASE or
				action==const.DELETE_DOCUMENT):
				requestResponse= self.deleteCall(url)

			elif(action==const.CREATE_DATABASE or
				action==const.UPDATE_SCHEMA or
				action==const.CREATE_DOCUMENT or
				action==const.WOQL_UPDATE):
				requestResponse=self.postCall(url,payload)

			if(requestResponse.status_code==200):
				print(requestResponse.url);
				return requestResponse.json() #if not a json not it raises an error
			#requestCall.raise_for_status()
		except requests.exceptions.RequestException as err:
			print ("Request Error",err)
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)