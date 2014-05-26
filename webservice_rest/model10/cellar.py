				#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from bson.objectid import ObjectId

from kardex import Kardex
from product import Product
from bson import json_util

import time
import datetime

class Cellar(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self._description = ''
		self.collection = db.cellar

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

		data = db.kardex.find({"cellar_identifier":self.identifier})

		data = db.kardex.aggregate([
			{"$match":
				{"cellar_identifier":self.identifier}
			},{
			"$group":
			{"_id":{ "product_sku":"$product_sku"}}
			}])

		kardex = Kardex()

		total_units = 0

		for x in data["result"]:
			product = x["_id"]["product_sku"]
			kardex.FindKardex(product, self.identifier)

			total_units += kardex.balance_units
		
		return int(total_units)

	def GetTotalPrice(self):
		data = db.kardex.find({"cellar_identifier":self.identifier})

		data = db.kardex.aggregate([
			{"$match":
				{"cellar_identifier":self.identifier}
			},{
			"$group":
			{"_id":{ "product_sku":"$product_sku"}}
			}])

		kardex = Kardex()

		total_price = 0

		for x in data["result"]:
			product = x["_id"]["product_sku"]
			kardex.FindKardex(product, self.identifier)

			total_price += kardex.balance_total
		
		return int(total_price)

	#@return json
	def Print(self):
		try:
			me = {"_id":ObjectId(self.identifier),
				"name" : self.name,
				"description": self.description,
				"total_price": self.GetTotalPrice(),
				"total_units": self.GetTotalUnits()}

			return me
		except:
			return self.ShowError("failed to print cellar")

	## validates and save cellar, it could be validated by name
	def Save(self):
		try:

			## validate if already exists a cellar with this name
			data_name = self.collection.find({"name": self.name})
			if data_name.count() >= 1:
				self.identifier = str(self.collection.update(
					{"_id":data_name[0]["_id"]},
					{"$set": {
						"name" : self.name,
						"description" : self.description
					}}))

				self.InitById(str(data_name[0]["_id"]))

				return self.ShowSuccessMessage(data_name[0]["_id"])

			##validate if the identifier exists
			if self.identifier == "":
				self.identifier = str(self.collection.insert({
					"name": self.name,
					"description": self.description
					}))

				self.InitById(self.identifier)

				return self.ShowSuccessMessage(self.identifier)

			data = self.collection.find({"_id":ObjectId(self.identifier)})

			if data.count() >= 1:
				self.identifier = str(self.collection.update(
					{"_id":data[0]["_id"]},
					{"$set": {
						"name" : self.name,
						"description" : self.description
					}}))
				self.InitById(self.identifier)

			return self.ShowSuccessMessage(str(object_id))
		except Exception, e:
			print str(e)
			return self.ShowError("failed to save cellar " + self.name)

	def GetList(self, page, items):
		#validate inputs
		page = int(page)
		items = int(items)
		data = self.collection.find().skip((page-1)*items).limit(items)

		data_rtn = [] ## return this data

		for d in data:

			cellar = Cellar()
			cellar.identifier = str(d["_id"])
			cellar.name = d["name"]
			cellar.description = d["description"]

			data_rtn.append(cellar.Print())
		return data_rtn

	### WARNING: this method is not opmitimized
	#@return direct database collection
	@staticmethod
	def GetAllCellars():
		data = db.cellar.find()

		data_rtn = [] ## return this data

		for d in data:

			cellar = Cellar()
			cellar.identifier = str(d["_id"])
			cellar.name = d["name"]
			cellar.description = d["description"]

			data_rtn.append(cellar.Print())
		return data_rtn

	def InitByName(self, name):
		try:
			datas = self.collection.find({"name": name})

			if datas >= 1:
				data = datas[0]
				self.identifier = str(data["_id"])
				self.name = data["name"]
				self.description = data["description"]

				return self.ShowSuccessMessage("cellar initialized")
			else:
				raise
		except:
			return self.ShowError("item not found")

	def InitById(self, idd):
		try:
			datas = self.collection.find({"_id": ObjectId(idd)})

			if datas >= 1:
				data = datas[0]
				self.identifier = str(data["_id"])
				self.name = data["name"]
				self.description = data["description"]

				return self.ShowSuccessMessage("cellar initialized")
			else:
				raise
		except:
			return self.ShowError("item not found")

	def ListProducts(self, page, items):
		data = db.kardex.find({"cellar_identifier":self.identifier})

		data = db.kardex.aggregate([
			{"$match":
				{"cellar_identifier":self.identifier}
			},{
				"$group":
					{"_id":{ "product_sku":"$product_sku"}}
			}])

		rtn_data = []

		kardex = Kardex()

		for x in data["result"]:
			product = Product()
			product.InitBySku(str(x["_id"]["product_sku"]))
			#print "idddddddddd"+str(x["_id"]["product_sku"])
			prod_print = product.Print()
			#print "product print "+json_util.dumps(prod_print)

			if "error" not in prod_print:
				kardex.FindKardex(str(prod_print["sku"]), self.identifier)
				prod_print["balance_units"] = kardex.balance_units
				prod_print["balance_price"] = kardex.balance_price
				prod_print["balance_total"] = kardex.balance_total

				rtn_data.append(prod_print)
		
		return rtn_data

	def ListKardex(self, page, items, day, fromm, until):

		if day == "today":
			now = datetime.datetime.now()
			yesterday = now - datetime.timedelta(days=1)
		if day == "yesterday":
			now = datetime.datetime.now() - datetime.timedelta(days=1)
			yesterday = now - datetime.timedelta(days=2)

		if day == "today" or day == "yesterday":

			start_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
			end_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
			oid_start = ObjectId.from_datetime(start_date)
			oid_stop = ObjectId.from_datetime(end_date)

			str_query = '{ "$and" : [{"operation_type":"sell"},{ "_id" : { "$gte" : { "$oid": "%s" }, "$lt" : { "$oid": "%s" } } }]}' % ( str(oid_start), str(oid_stop) )
			data = db.kardex.find( json_util.loads(str_query) )
			return data
 			
		if day == "period":

			ffrom=fromm.split("-")

			from_y=int(ffrom[0])
			from_m=int(ffrom[1])
			from_d=int(ffrom[2])

			untill= until.split("-")

			until_y=int(untill[0])
			until_m=int(untill[1])
			until_d=int(untill[2])

			# now = datetime.datetime.now()
			# yesterday = now - datetime.timedelta(days=30)	

			start_date = datetime.datetime(from_y, from_m, from_d, 0, 0, 0)
			end_date = datetime.datetime(until_y, until_m, until_d, 23, 59, 59)
			oid_start = ObjectId.from_datetime(start_date)
			oid_stop = ObjectId.from_datetime(end_date)

			str_query = '{ "$and" : [{"operation_type":"sell"},{ "_id" : { "$gte" : { "$oid": "%s" }, "$lt" : { "$oid": "%s" } } }]}' % ( str(oid_start), str(oid_stop) )
			data = db.kardex.find( json_util.loads(str_query) )
			return data

	def Rename(self, new_name):
		try:

			if new_name == "":
				raise

			self.collection.update({"_id":ObjectId(self.identifier)},
				{"$set":{
					"name":new_name
				}})
			self.name = new_name
			self.ShowSuccessMessage("name changed correctly")
		except:
			self.ShowError("error changing name")
