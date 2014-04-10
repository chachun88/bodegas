#!/usr/bin/env python

from basemodel import BaseModel

class Brand(BaseModel):

	def __init__(self):
		self._identifier	= ""
		self._name			= ""

	def Save(self, collection):

		# validate identifier
		data = collection.find({"identifier" : self.identifier})
		if data.count() >= 1:

			collection.update(
				{"_id" : data[0]["_id"]},
				{"$set" : {
					"identifier" : self.identifier,
					"name" : self.name
				}})

			return str(data[0]["_id"])

		#save the object and return the id
		object_id = collection.insert(
			{
			"identifier" : self.identifier,
			"name" : self.name
			})

		return str(object_id)

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