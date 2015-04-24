#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2

from basehandler import BaseHandler
from bson import json_util

from model10.base_model import BaseModel

class Brand(BaseModel):

	def __init__(self):
		BaseModel.__init__(self)
		self._identifier=""
		self._name=""

	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value
			
	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value


	def InitWithId(self, idd):
		url = self.wsurl() + "/brand/find"

		url += "?token=" + self.token
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.identifier = str(data["id"])
		self.name = data["name"]

	def InitWithName(self, name):
		url = self.wsurl() + "/brand/find"

		url += "?token=" + self.token
		url += "&name=" + name

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.identifier = str(data["id"])
		self.name = data["name"]	

	def Remove(self):
		if self.identifier!="":
			url=self.wsurl() + "/brand/remove"
			url+="?token=" + self.token
			url+="&id=" + self.identifier

			urllib.urlopen(url)	

	def Save(self):
		url = self.wsurl()+"/brand/add?token=" + self.token

		url += "&name=" + self.name		
		url += "&id=" + self.identifier

		return urllib.urlopen(url).read()

	def get_product_list(self):
			
		url = self.wsurl()+"/brand/list?token=" + self.token + "&items=100"
		content = urllib2.urlopen(url).read()

		# parse content to array data
		data = json_util.loads(content)

		self.identifier = data

		return data

	def Search(self, query):
		url = self.wsurl() + "/brand/search?token=" + self.token
		url += "&q=" + query
		return urllib.urlopen(url).read()