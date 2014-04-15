#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

class Category(BaseModel):
	def __init__(self, db):
		super(BaseModel, self).__init__(db)
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

	@staticmethod
	def GetAllCategories():
		return ''
