#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model.base_model import BaseModel
from bson import json_util
import urllib

class Shipping(BaseModel):

	def __init__(self):
		BaseModel.__init__(self)
		self._identifier = ""
		self._to_city_id = 0
		self._from_city_id = 0
		self._edited = False

	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value

	@property
	def from_city_id(self):
	    return self._from_city_id
	@from_city_id.setter
	def from_city_id(self, value):
	    self._from_city_id = value

	@property
	def to_city_id(self):
	    return self._to_city_id
	@to_city_id.setter
	def to_city_id(self, value):
	    self._to_city_id = value

	@property
	def correos_price(self):
	    return self._correos_price
	@correos_price.setter
	def correos_price(self, value):
	    self._correos_price = value

	@property
	def chilexpress_price(self):
	    return self._chilexpress_price
	@chilexpress_price.setter
	def chilexpress_price(self, value):
	    self._chilexpress_price = value

	@property
	def price(self):
	    return self._price
	@price.setter
	def price(self, value):
	    self._price = value
	

	@property
	def edited(self):
	    return self._edited
	@edited.setter
	def edited(self, value):
	    self._edited = value
	
	
	def Save(self):

		url = self.wsurl() + "/shipping/save"

        data = {
        "token":self.token,
        "from_city_id":self.from_city_id,
        "to_city_id":self.to_city_id,
        "identifier":self.identifier,
        "correos_price":self.correos_price,
        "chilexpress_price":self.chilexpress_price,
        "price":self.price,
        "edited":self.edited
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj
	
	
	