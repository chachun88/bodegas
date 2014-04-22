#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class Brand(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	def InitById(self, idd):
		return ''

	def Save(self):
		return ''

	def GetAllBrands(self):
		return ''

	def InitByName(self, name):
		return ''
