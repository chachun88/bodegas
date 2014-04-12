#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

Class Cellar(BaseModel):
	def __init__(self):
		super(BaseModel, self).__init__()
		self._identifier = ''
		self._name = ''
		self._attribute = ''

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
	def attribute(self):
		return self._attribute
	@attribute.setter
	def attribute(self, value):
		self._attribute = value

	def GetTotalUnits(self):
		return ''

	def GetTotalPrice(self):
		return ''

	def Remove(self):
		return ''

	def Save(self):
		return ''

	def GetAllCellars(self):
		return ''
