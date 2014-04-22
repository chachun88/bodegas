#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class Cellar(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._description = ''

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def description(self):
		return self._description
	@description.setter
	def description(self, value):
		self._description = value

	def GetTotalUnits(self):
		return ''

	def GetTotalPrice(self):
		return ''

	def Save(self):
		return ''

	def GetAllCellars(self):
		return ''

	def InitById(self, idd):
		return ''

	def Print(self):
		return ''

	def Rename(self, new_name):
		return ''

	def ListProducts(self, page, items):
		return ''
