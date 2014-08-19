#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel, db

class OrderDetail(BaseModel):

	@property
	def id(self):
	    return self._id
	@id.setter
	def id(self, value):
	    self._id = value
	
	@property
	def order_id(self):
	    return self._order_id
	@order_id.setter
	def order_id(self, value):
	    self._order_id = value
	
	@property
	def product_id(self):
	    return self._product_id
	@product_id.setter
	def product_id(self, value):
	    self._product_id = value
	
	@property
	def quantity(self):
	    return self._quantity
	@quantity.setter
	def quantity(self, value):
	    self._quantity = value
	
	@property
	def total(self):
	    return self._total
	@total.setter
	def total(self, value):
	    self._total = value
	

	def __init__(self):
		self.collection = db.order_detail
		self._id	= ""
		self._order_id 	= ""
		self._quantity	= ""
		self._product_id = ""
		self._total 	= ""

	def Save(self):
		#save the object and return the id


		new_id = db.seq.find_and_modify(query={'seq_name':'order_detail_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

		object_id = self.collection.insert(
			{
			"id":new_id,
			"order_id":self.order_id,
			"quantity":self.quantity,
			"product_id":self.product_id,
			"total":self.total
			})

		return str(object_id)

	def ListByOrderId(self, order_id, page=1, limit=20):

		skip = (int(page) - 1) * int(limit)

		order_detail = self.collection.find({"order_id":order_id}).skip(skip).limit(int(limit))

		return json_util.dumps(order_detail)

	def GetDetail(self, _id):

		order_detail = self.collection.find_one({"id":_id})

		return json_util.dumps(order_detail)