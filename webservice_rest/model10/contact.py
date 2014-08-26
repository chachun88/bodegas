#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel, db

class Contact(BaseModel):

	@property
	def id(self):
		return self._id
	@id.setter
	def id(self, value):
		self._id = value

	@property
	def customer_id(self):
		return self._customer_id
	@customer_id.setter
	def customer_id(self, value):
		self._customer_id = value

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value
	
	@property
	def type(self):
		return self._type
	@type.setter
	def type(self, value):
		self._type = value
	
	@property
	def address(self):
		return self._address
	@address.setter
	def address(self, value):
		self._address = value
	
	@property
	def telephone(self):
		return self._telephone
	@telephone.setter
	def telephone(self, value):
		self._telephone = value
	
	@property
	def email(self):
		return self._email
	@email.setter
	def email(self, value):
		self._email = value

	def __init__(self):
		self.collection = db.contact
		self._id = ""
		self._name = ""
		self._type = ""
		self._telephone = ""
		self._email = ""
		self._address = ""
		self._customer_id = ""

	def InitById(self, _id):

		contact = self.collection.find_one({"id":int(_id)})

		if contact:
			return contact
		else:
			return ""

	def Save(self):

		new_id = db.seq.find_and_modify(query={'seq_name':'contact_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

		contact = {
		"id": new_id,
		"name": self.name,
		"type": self.type,
		"telephone": self.telephone,
		"email": self.email,
		"customer_id": self.customer_id,
		"address": self.address
		}

		try:

			self.collection.insert(contact)

			return new_id

		except Exception, e:

			return str(e)

	def Edit(self):

		print "Edit WS id:{}\n".format(self.id)

		contact = {
		"name": self.name,
		"type": self.type,
		"telephone": self.telephone,
		"email": self.email,
		"customer_id": self.customer_id,
		"address":self.address
		}

		try:
			self.collection.update({"id":int(self.id)},{"$set":contact})
			return self.id
		except Exception, e:

			return str(e)

	def ListByCustomerId(self, _customer_id):

		contacts = self.collection.find({"customer_id":_customer_id})

		if contacts:
			return contacts
		else:
			return []

	def Remove(self,ids):
		print ids
		self.collection.remove({"id":{"$in":[int(n) for n in ids.split(",")]}})
	