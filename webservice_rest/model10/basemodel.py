#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymongo

from bson import json_util
from bson.objectid import ObjectId

# database_connection
connection 	= pymongo.Connection("localhost", 27017)
db 			= connection.market_tab

class BaseModel(object):
	def __init__(self):
		self._identifier = ''
		self._collection = db.base_testing ## mongodb collection

	@property
	def identifier(self):
		return self._identifier
	@identifier.setter
	def identifier(self, value):
		self._identifier = value

	@property
	def collection(self):
		return self._collection
	@collection.setter
	def collection(self, value):
		self._collection = value

	def Save(self):
		return ShowError("must be overriden by user")

	def InitById(self, idd):
		return ShowError("must be overriden by user")

	#@return json object
	def GetList(self, page, items):

		#validate inputs
		page = int(page)
		items = int(items)
		return self.collection.find().skip((page-1)*items).limit(items)

	#@return integer
	def GetPages(self, limit):
		try:
			items = int(limit)
			items = self.collection.find().count() / items

			return items
		except Exception, e:
			return 0

	#@return json object
	def Remove(self):
		try:
			## raise exception if identifier is empty
			if self.identifier == "":
				raise

			self.collection.remove({"_id":ObjectId(self.identifier)})

			return self.ShowSuccessMessage("object: " + self.identifier + " has been deleted")
		except Exception, e:
			return self.ShowError("object: not found")

	#@return json object
	def ShowError(self, error_text):
		return {'error': error_text}

	#@return json object
	def ShowSuccessMessage(self, message):
		return {'success': message}
