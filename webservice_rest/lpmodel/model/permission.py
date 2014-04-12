#!/usr/bin/python
# -*- coding: UTF-8 -*-

Class Permission(object):
	def __init__(self):
		super(object, self).__init__()
		self._identifier = ''
		self._name = ''

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

	def GetAllPermisions(self):
		return ''
