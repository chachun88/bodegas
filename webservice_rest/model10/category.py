#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
from bson.objectid import ObjectId

class Category(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._parent = ''

		self.collection = db.category

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def parent(self):
	    return self._parent
	@parent.setter
	def parent(self, value):
	    self._parent = value

	def Print(self):
		return {
				"name":self.name,
				"parent":self.parent,
				"_id":ObjectId(self.identifier)}

	def InitByName(self, name):

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = '''select * from "Brand" where name = %(name)s'''
		parameters = {
		"name":name
		}
		cur.execute(query,parameters)
		category = cur.fetchone()

		if category:
			self.name = category["name"]
			self.parent = category["parent"]
			self.id = category["id"]
			return self.ShowSuccessMessage("category correctly initialized")
		else:
			return self.ShowError("category can not be initialized")

		# try:
		# 	categories = self.collection.find({"name":name})

		# 	if categories.count() >= 1: 
		# 		self.name = categories[0]["name"]
		# 		self.parent = categories[0]["parent"]
		# 		self.identifier = str(categories[0]["_id"])
		# 		return self.ShowSuccessMessage("category correctly initialized")
		# 	else:
		# 		raise
		# except:
		# 	return self.ShowError("category can not be initialized")

	def InitById(self, idd):
		# try: 
		# 	categories = self.collection.find({"_id":ObjectId(idd)})

		# 	if categories.count() >= 1: 
		# 		self.name = categories[0]["name"]
		# 		self.parent = categories[0]["parent"]
		# 		self.identifier = str(categories[0]["_id"])
		# 	return self.ShowSuccessMessage("category correctly initialized")
		# except:
		# 	return self.ShowError("category can not be initialized")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = '''select * from "Brand" where id = %(id)s'''
		parameters = {
		"id":idd
		}
		cur.execute(query,parameters)
		category = cur.fetchone()

		if category:
			self.name = category["name"]
			self.parent = category["parent"]
			self.id = category["id"]
			return self.ShowSuccessMessage("category correctly initialized")
		else:
			return self.ShowError("category can not be initialized")

	def Save(self):
		# try:
		# 	data = self.collection.find({"name":self.name})
		# 	if data.count() >= 1:
		# 		self.collection.update({
		# 			"name":self.name
		# 			},{
		# 			"$set":{
		# 				"name" : self.name,
		# 				"parent":self.parent
		# 				}
		# 			})
		# 		self.identifier = str(data[0]["_id"])

		# 	else:
		# 		self.collection.save({
		# 			"name":self.name,
		# 			"parent":self.parent
		# 			})

		# 		data = self.collection.find({"name":self.name})
		# 		self.identifier = str(data[0]["_id"])

		# 	return self.ShowSuccessMessage("category saved correctly")
		# except:
		# 	return self.ShowError("error saving category")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		query = '''select * from "Brand" where name = %(name)s'''
		parameters = {
		"name":name
		}
		cur.execute(query,parameters)
		category = cur.fetchone()

		if category:
			query = '''update 

	def GetAllCategories(self):
		return self.collection.find()

	def Exist(self, name):
		print "aa"
		if self.collection.find({"name":name}).count() >= 1:
			return True
		return False

