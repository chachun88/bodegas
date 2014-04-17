#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel

class Salesman(BaseModel):

	def __init__(self):
		self._identifier	= ""
		self._name			= ""
		self._password		= ""
		self._email			= ""
		self._permissions	= ""

	def Save(self, collection):

		# validate identifier

		data = collection.find({"email" : self.email})
		if data.count() >= 1:

			collection.update(
				{"_id" : data[0]["_id"]},
				{"$set" : {
					"name" 		: self.name,
					"password"  : self.password,
					"email" 	: self.email,
					"permissions":self.permissions
				}})

			return str(data[0]["_id"])

		#save the object and return the id
		object_id = collection.insert(
			{
			"name" 		: self.name,
			"password"  : self.password,
			"email"  	: self.email,
			"permissions": self.permissions
			})

		return str(object_id)

	def FindByEmail(self, email, collection):
		data = collection.find({"email":email})

		return str(json_util.dumps(data[0]))

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
	
	@property
	def password(self):
	    return self._password
	@password.setter
	def password(self, value):
	    self._password = value

	@property
	def email(self):
	    return self._email
	@email.setter
	def email(self, value):
	    self._email = value

	@property
	def permissions(self):
	    return self._permissions
	@permissions.setter
	def permissions(self, value):
	    self._permissions = value
	
