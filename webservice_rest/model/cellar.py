#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

from bson.objectid import ObjectId
from bson import json_util

class Cellar(BaseModel):

	""" docstring for Cellar """
	def __init__(self):
		self._name = ""
		self._description = ""
		self._identifier = ""
		pass

	def Save(self, collection):

		if self.identifier == "":
			data = collection.insert({
				"name": self.name,
				"description": self.description
				})

			return str(data)

		data = collection.find({"_id":ObjectId(self.identifier)})

		if data.count() >= 1:
			collection.update(
				{"_id":data[0]["_id"]},
				{"$set": {
					"name" : self.name,
					"description" : self.description
				}})

		return str(data[0]["_id"])

	def Remove(self, collection):
		self.RemoveById(self.identifier, collection)
		return "ok"

	def AddProducts(self, product_list, collection):
		try:
			products = product_list.split(",")
			for p in products:
				## detect if the combination exists

				product = p.split(":")
				combination = collection.find({
										"product_id":ObjectId(product[0]),
										"cellar_id":ObjectId(self.identifier)})

				if combination.count() >= 1:
					## sum 1 to quantity
					quantity = combination[0]["quantity"]
					quantity += int(product[1])

					## update quantity
					collection.update({"_id":ObjectId(combination[0]["_id"])},
									{"$set":{"quantity":quantity}})
				else:
					collection.insert({
										"product_id":ObjectId(product[0]),
										"cellar_id":ObjectId(self.identifier),
										"quantity":int(product[1]),
									})

			return "ok"

		except Exception, e:
			return "error ocurred" 

	def RemoveProducts(self, product_list, collection):
		try:
			products = product_list.split(",")

			for p in products:
				##detect if the combination exists
				product = p.split(":")

				combination = collection.find({
							"product_id":ObjectId(p),
							"cellar_id":ObjectId(self.identifier)
							})

				if combination.count() >= 1:
					##rest 1 to quantity
					quantity = combination[0]["quantity"]
					quantity -= int(product[1])

					##update quantity
					collection.update({"_id":ObjectId(combination[0]["_id"])},
									{"$set":{"quantity":quantity}})

		except Exception, e:
			return "error ocurred"

	def ListProducts(self, page, items, db_cellar_prod, db_products):

		data = db_cellar_prod.find({"cellar_id":ObjectId(self.identifier)}).limit(int(items)).skip(int((page-1) * items)) ## solving pagination
		products = []

		for d in data:
			## adding products
			product_id = d["product_id"]
			product = db_products.find_one({"_id":ObjectId(product_id)})

			products.append(product)

		return json_util.dumps(products)

	def InitWithId(self, idd, collection):
		datas = collection.find({"_id": ObjectId(idd)})

		if datas >= 1:
			data = datas[0]
			self.identifier = data["_id"]
			self.name = data["name"]
			self.description = data["description"]
		else:
			print "item not found"

	def Print(self):
		me = {"_id":ObjectId(self.identifier),
			"name" : self.name,
			"description": self.description}

		return json_util.dumps(me)

	@staticmethod
	def List(page, items, collection):
		return json_util.dumps(collection.find().skip((page-1) * items).limit(items))

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

	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = str(value)
	
