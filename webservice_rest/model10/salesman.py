#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from salesmanpermission import SalesmanPermission
from bson.objectid import ObjectId


class Salesman(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self.collection = db.salesman
		self._salesman_id = ''
		self._name = ''
		self._password = '' 
		self._email = ''
		self._permissions = []

	@property
	def salesman_id(self):
	    return self._salesman_id
	@salesman_id.setter
	def salesman_id(self, value):
	    self._salesman_id = value
	

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
	

	def Print(self):
		return {
			"_id":ObjectId(self.identifier),
			"name":self.name,
			"email":self.email,
			"password":self.password,
			"permissions":self.permissions,
			"salesman_id":self.salesman_id
		}

	def Remove(self):
		try:
			#delete = self._permissions.RemoveAllByUser()
			#if "error" in delete:
			#	return delete

			return BaseModel.Remove(self)
		except Exception, e:
			return self.ShowError("error removing user")

	def Login(self, username, password):
		data = self.collection.find({"email":username, "password":password})

		if data.count() >= 1:
			self.InitByEmail(username) ## init user
			return True
		return False

	def InitByEmail(self, email):

		try:
			data = self.collection.find({"email":email})
			if data.count() >= 1:
				self.name 		= data[0]["name"]
				self.password 	= data[0]["password"]
				self.email 		= email
				self.identifier = str(data[0]["_id"])
				self.permissions= data[0]["permissions"]
				self.id         = data[0]["salesman_id"]

				return self.ShowSuccessMessage("user initialized")
			else:
				raise
		except Exception, e:
			return self.ShowError("user : " + email + " not found")

	def InitById(self, idd):

		try:
			data = self.collection.find({"_id":ObjectId(idd)})
			if data.count() >= 1:
				self.name 		= data[0]["name"]
				self.password 	= data[0]["password"]
				self.email 		= data[0]["email"]
				self.identifier = str(data[0]["_id"])
				self.permissions=  data[0]["permissions"]
				self.id         = data[0]["salesman_id"]

				return self.ShowSuccessMessage("user initialized")
			else:
				raise
		except Exception, e:
			return self.ShowError("user : " + idd + " not found")

	def GetPermissions(self):
		return self._permissions.FindPermissions(self.identifier)


	def AssignPermission(self, permission):
		## TODO: validate if permission exist
		self._permissions.salesman_identifier 	= self.identifier
		self._permissions.permission_identifier = permission
		return self._permissions.Save()


	def RemovePermission(self, permission):
		self._permissions.salesman_identifier = self.identifier
		self._permissions.permission_identifier = permission
		return self._permissions.RemovePermission()

	def Save(self):
		try:
			# validate identifier
			data = self.collection.find({"email" : self.email})

			new_id = db.seq.find_and_modify(query={'seq_name':'salesman_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True)["id"]

			if data.count() >= 1:

				self.identifier = str(self.collection.update(
					{"_id" : data[0]["_id"]},
					{"$set" : {
						"name" 		: self.name,
						"password"  : self.password,
						"email" 	: self.email,
						"permissions": self.permissions
					}}))

				return self.ShowSuccessMessage(str(data[0]["_id"]))

			#save the object and return the id
			object_id = self.collection.insert(
				{
				"salesman_id": new_id,
				"name" 		: self.name,
				"password"  : self.password,
				"email"  	: self.email,
				"permissions": self.permissions
				})

			self.identifier = str(object_id)

			return self.ShowSuccessMessage(str(object_id))
		except Exception, e:
			return self.ShowError("failed to save user " + self.email)
