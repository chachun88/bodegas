#access_token.py
# TODO: generar access token con oauth

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# from pymongo import Connection
from datetime import date
from base_handler import BaseHandler
from model10.basemodel import BaseModel

import datetime

class AccessTokenHandler(BaseHandler):
	
	def get(self):

		# getting the appid
		appid 	= ""
		token 	= ""
		now 	= ""

		try:
			appid = self.get_argument("appid")
		except Exception, e:
			pass


		# validate appid
		if appid == "":
			self.write('{"error": "appid not found"}')
			return

		# TODO: must validate appid and permissions on database

		bm = BaseModel()
		response_obj = bm.GetAccessToken(appid)

		if "success" in response_obj:
			self.write("{}".format(response_obj["success"]))
		else:
			self.write("{}".format(response_obj["error"]))
