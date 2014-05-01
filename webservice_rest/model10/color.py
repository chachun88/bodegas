#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId

class Color(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._idd = ''

		self.collection = db.color
		db.system_js.counter = 'function(name){ var ret = db.counters.findAndModify({query:{_id:name}, update:{$inc:{next:1}}, "new":true, upsert:true}); return ret.next; }'

	@property
	def idd(self):
	    return self._idd
	@idd.setter
	def idd(self, value):
	    self._idd = value
		
	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	def Print(self):
		return {
				"name":self.name,
				"idd":self.idd,
				"_id":ObjectId(self.identifier)}

	def InitByName(self, name):
		try:
			colors = self.collection.find({"name":name})

			if colors.count() >= 1: 
				self.name = colors[0]["name"]
				self.idd = colors[0]["idd"]
				self.identifier = str(colors[0]["_id"])
				return self.ShowSuccessMessage("color correctly initialized")
			else:
				raise
		except:
			return self.ShowError("color can not be initialized")

	def InitById(self, idd):
		try: 
			colors = self.collection.find({"_id":ObjectId(idd)})

			if colors.count() >= 1: 
				self.name = colors[0]["name"]
				self.idd = colors[0]["idd"]
				self.identifier = str(colors[0]["_id"])
			return self.ShowSuccessMessage("color correctly initialized")
		except:
			return self.ShowError("color can not be initialized")

	def Save(self):
		try:
			data = self.collection.find({"name":self.name})			
			if data.count() >= 1:
				self.collection.update({
					"name":self.name
					},{
					"$set":{
						"name" : self.name,
						#"idd":self.idd
						}
					})
				self.identifier = str(data[0]["_id"])

			else:
				count=db.system_js.counter("color")
				self.collection.save({
					"name":self.name,
					"idd":count
					})

				data = self.collection.find({"name":self.name})
				self.identifier = str(data[0]["_id"])

			return self.ShowSuccessMessage("color saved correctly")
		except:
			return self.ShowError("error saving color")

	def GetAllColors(self):
		return self.collection.find()

	def Exist(self, name):
		if self.collection.find({"name":name}).count() >= 1:
			return True
		return False
