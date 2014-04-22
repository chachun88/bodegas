#!/usr/bin/python
# -*- coding: UTF-8 -*-

class BaseModel(object):
	def __init__(self):
		object.__init__(self)
		self._identifier = ''
		self._collection = ''

	@property
	def identifier(self):
		return self._identifier
	@identifier.setter
	def identifier(self, value):
		self._identifier = value

	@property
	def collection(self):
		return self._collection
	@collection.setter
	def collection(self, value):
		self._collection = value

	def Save(self):
		return ''

	def InitById(self, idd):
		return ''

	def GetList(self, page, items):
		return ''

	def GetPages(self, limit):
		return ''

	def Remove(self):
		return ''

	def ShowError(self, error_text):
		return ''

	def ShowSuccessMessage(self, message):
		return ''
