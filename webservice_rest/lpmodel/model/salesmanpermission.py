#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class SalesmanPermission(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._salesman_identifier = ''
		self._permission_identifier = ''

	@property
	def salesman_identifier(self):
		return self._salesman_identifier
	@salesman_identifier.setter
	def salesman_identifier(self, value):
		self._salesman_identifier = value

	@property
	def permission_identifier(self):
		return self._permission_identifier
	@permission_identifier.setter
	def permission_identifier(self, value):
		self._permission_identifier = value

	def Save(self):
		return ''

	def FindPermissions(self, sales_man_id):
		return ''

	def RemovePermission(self):
		return ''

	def RemoveAllByUser(self):
		return ''
