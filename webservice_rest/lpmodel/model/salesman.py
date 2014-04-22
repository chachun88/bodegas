#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class Salesman(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._password = ''
		self._email = ''

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

	def Login(self, username, password):
		return ''

	def InitByEmail(self, email):
		return ''

	def GetPermissions(self):
		return ''

	def AssignPermission(self, permission):
		return ''

	def Save(self):
		return ''

	def RemovePermission(self, permission):
		return ''
