#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from salesmanpermission import SalesmanPermission


class Salesman(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self.collection = db.salesman
		self._name = ''
		self._password = ''
		self._email = ''

		self._permissions = SalesmanPermission() #private

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

	def Remove(self):
		try:
			delete = self._permissions.RemoveAllByUser()
			if "error" in delete:
				return delete

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

				return self.ShowSuccessMessage("user initialized")
			else:
				raise
		except Exception, e:
			return self.ShowError("user : " + email + " not found")

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
			if data.count() >= 1:

				self.identifier = str(self.collection.update(
					{"_id" : data[0]["_id"]},
					{"$set" : {
						"name" 		: self.name,
						"password"  : self.password,
						"email" 	: self.email
					}}))

				return self.ShowSuccessMessage(str(data[0]["_id"]))

			#save the object and return the id
			object_id = self.collection.insert(
				{
				"name" 		: self.name,
				"password"  : self.password,
				"email"  	: self.email
				})

			self.identifier = str(object_id)

			return self.ShowSuccessMessage(str(object_id))
		except Exception, e:
			return self.ShowError("failed to save user " + self.email)
