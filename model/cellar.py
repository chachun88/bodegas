#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

class Cellar(BaseModel):

	""" docstring for Cellar """
	def __init__(self):
		self._name = ""
		self._description = ""
		self._identifier = ""
		pass

	def Save(self):
		url = self.wsurl() + "/cellar/add"
		url += "?token=" + self.token()
		url += "&name=" + self.name
		url += "&description=" + self.description

		return urllib.urlopen(url).read()

	def Remove(self):
		url = self.wsurl() + "/cellar/remove"
		url += "?token=" + self.token()
		url += "&id=" + self.identifier

		print url

		return urllib.urlopen(url).read()

	def AddProducts(self):
		pass

	def RemoveProducts(self):
		pass

	def ListProducts(self):
		pass

	def InitWithId(self, idd):
		url = self.wsurl() + "/cellar/find"
		url += "?token=" + self.token()
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		json_data = json_util.loads(json_string)

		self.identifier = str(json_data["_id"])
		self.name = json_data["name"]
		self.description = json_data["description"]

	def List(self, page, items):
		url = self.wsurl() + "/cellar/list"
		url += "?token=" + self.token()
		url += "&page={}".format(page)
		url += "&items={}".format(items)

		json_string = urllib.urlopen(url).read()
		return json_util.loads(json_string)
	

	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value
	
	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self, value):
	    self._description = value
	
	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value
	