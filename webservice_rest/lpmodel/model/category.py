#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class Category(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._parent = ''

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def parent(self):
		return self._parent
	@parent.setter
	def parent(self, value):
		self._parent = value

	def InitById(self, idd):
		return ''

	def Save(self):
		return ''

	def GetAllCategories(self):
		return ''

	def InitByName(self):
		return ''
