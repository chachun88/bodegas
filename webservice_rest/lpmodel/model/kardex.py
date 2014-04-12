#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

Class Kardex(BaseModel):
	def __init__(self):
		super(BaseModel, self).__init__()
		self._identifier = ''
		self._product_identifier = ''
		self._cellar_identifier = ''
		self._operation_type = ''
		self._units = ''
		self._price = ''
		self._total = ''
		self._balance_units = ''
		self._balance_price = ''
		self._balance_total = ''

	@property
	def identifier(self):
		return self._identifier
	@identifier.setter
	def identifier(self, value):
		self._identifier = value

	@property
	def product_identifier(self):
		return self._product_identifier
	@product_identifier.setter
	def product_identifier(self, value):
		self._product_identifier = value

	@property
	def cellar_identifier(self):
		return self._cellar_identifier
	@cellar_identifier.setter
	def cellar_identifier(self, value):
		self._cellar_identifier = value

	@property
	def operation_type(self):
		return self._operation_type
	@operation_type.setter
	def operation_type(self, value):
		self._operation_type = value

	@property
	def units(self):
		return self._units
	@units.setter
	def units(self, value):
		self._units = value

	@property
	def price(self):
		return self._price
	@price.setter
	def price(self, value):
		self._price = value

	@property
	def total(self):
		return self._total
	@total.setter
	def total(self, value):
		self._total = value

	@property
	def balance_units(self):
		return self._balance_units
	@balance_units.setter
	def balance_units(self, value):
		self._balance_units = value

	@property
	def balance_price(self):
		return self._balance_price
	@balance_price.setter
	def balance_price(self, value):
		self._balance_price = value

	@property
	def balance_total(self):
		return self._balance_total
	@balance_total.setter
	def balance_total(self, value):
		self._balance_total = value

	def Save(self):
		return ''
