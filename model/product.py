#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2
import pprint

from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

class Product(BaseModel):

#	def get_product_list(self):
#		return [{"name":"p1"},{"name":"p2"},{"name":"p3"}]

	def __init__(self):
		self._identifier=""
		self._category=""
		self._sku=""
		self._name=""
		self._upc=""		
		self._description=""
		self._brand=""
		self._manufacturer=""
		self._size=[]
		self._color=[]
		self._material=""
		self._bullet_1=""
		self._bullet_2=""
		self._bullet_3=""
		self._currency=""
		self._price=""
		self._image=""
		self._image_2=""
		self._image_3=""		
		

	####################
	### Class fields ###
	####################	

	@property
	def identifier(self):
	    return self._identifier
	@identifier.setter
	def identifier(self, value):
	    self._identifier = value	

	@property
	def category(self):
	    return self._category
	@category.setter
	def category(self, value):
	    self._category = value	    
	
	@property
	def sku(self):
	    return self._sku
	@sku.setter
	def sku(self, value):
	    self._sku = value

	@property
	def name(self):
	    return self._name
	@name.setter
	def name(self, value):
	    self._name = value

	@property
	def upc(self):
	    return self._upc
	@upc.setter
	def upc(self, value):
	    self._upc = value
	
	@property
	def description(self):
	    return self._description
	@description.setter
	def description(self, value):
	    self._description = value
	
	@property
	def brand(self):
	    return self._brand
	@brand.setter
	def brand(self, value):
	    self._brand = value

	@property
	def manufacturer(self):
	    return self._manufacturer
	@manufacturer.setter
	def manufacturer(self, value):
	    self._manufacturer = value

	@property
	def size(self):
	    return self._size
	@size.setter
	def size(self, value):
	    self._size = value
	
	@property
	def color(self):
	    return self._color
	@color.setter
	def color(self, value):
	    self._color = value

	@property
	def material(self):
	    return self._material
	@material.setter
	def material(self, value):
	    self._material = value
	
	@property
	def bullet_1(self):
	    return self._bullet_1
	@bullet_1.setter
	def bullet_1(self, value):
	    self._bullet_1 = value
	
	@property
	def bullet_2(self):
	    return self._bullet_2
	@bullet_2.setter
	def bullet_2(self, value):
	    self._bullet_2 = value
	
	@property
	def bullet_3(self):
	    return self._bullet_3
	@bullet_3.setter
	def bullet_3(self, value):
	    self._bullet_3 = value    

	@property
	def currency(self):
	    return self._currency
	@currency.setter
	def currency(self, value):
	    self._currency = value
	
   	@property
	def price(self):
	    return self._price
	@price.setter
	def price(self, value):
	    self._price = value

	@property
	def image(self):
	    return self._image
	@image.setter
	def image(self, value):
	    self._image = value
	
	@property
	def image_2(self):
	    return self._image_2
	@image_2.setter
	def image_2(self, value):
	    self._image_2 = value
	
	@property
	def image_3(self):
	    return self._image_3
	@image_3.setter
	def image_3(self, value):
	    self._image_3 = value

	
	#################
	#### Methods ####
	#################

	def InitWithId(self, idd):
		url = self.wsurl() + "/product/find"

		url += "?token=" + self.token()
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.identifier = str(data["_id"])
		self.category = data["category"]
		self.sku = data["sku"]
		self.name = data["name"] 
		self.upc= data["upc"]
		self.description = data["description"]
		self.brand = data["brand"]
		self.manufacturer= data["manufacturer"]
		self.size=data["size"]
		self.color= data["color"]
		self.material = data["material"] 
		self.bullet_1=data ["bullet_1"]
		self.bullet_2=data ["bullet_2"]
		self.bullet_3=data ["bullet_3"]
		# self.currency=data ["currency"]
		self.price =data["price"]
		self.image = data ["image"]
		self.image_2 = data ["image_2"]
		self.image_3 = data ["image_3"]

	def InitWithSku(self, sku):
		url = self.wsurl() + "/product/find"

		url += "?token=" + self.token()
		url += "&sku=" + sku

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.identifier = str(data["_id"])
		self.category = data["category"]
		self.sku = data["sku"]
		self.name = data["name"] 
		self.upc= data["upc"]
		self.description = data["description"]
		self.brand = data["brand"]
		self.manufacturer= data["manufacturer"]
		self.size=data["size"]
		self.color= data["color"]
		self.material = data ["material"] 
		self.bullet_1=data ["bullet_1"]
		self.bullet_2=data ["bullet_2"]
		self.bullet_3=data ["bullet_3"]
		# self.currency=data ["currency"]
		self.price=data["price"]
		self.image = data ["image"]
		self.image_2 = data ["image_2"]
		self.image_3 = data ["image_3"]	


	def Remove(self):
		if self.identifier!="":
			url=self.wsurl() + "/product/remove"
			url+="?token=" + self.token()
			url+="&id=" + self.identifier

			urllib.urlopen(url)

	def Save(self, typee="other"):
		#siz={ 'size':[self.size] }
		#col={ 'color':[self.color] }

		descripcion = ""
		name = ""
		color = ""
		brand = ""

		try:
			descripcion = self.description.encode('utf-8')
		except:
			descripcion = self.description

		try:
			name = self.name.encode("utf-8")
		except:
			name = self.name

		try:
			color =  ",".join(v for v in self.color)
			# color =unicode(color, errors="ignore")
		except:
			color = ",".join(v.encode('utf-8') for v in self.color)				

		try:
			brand = self.brand.encode("utf-8")
		except:
			brand = self.brand

		url = self.wsurl()+"/product/add?token=" + self.token()

		if typee == "masive":
			url += "&category=" + unicode(self.category, errors="ignore")
			url += "&sku=" + unicode(self.sku, errors="ignore")
			url += "&name=" + unicode(name, errors="ignore")
			url += "&upc=" + unicode(self.upc, errors="ignore")
			url += "&description=" + unicode(descripcion, errors="ignore")
			url += "&brand=" + unicode(brand, errors="ignore")
			url += "&manufacturer=" + unicode(self.manufacturer, errors="ignore")
			url += "&size=" + ",".join(str(v) for v in self.size)
			url += "&color=" + unicode(color, errors="ignore")
			#url += "&material=" + self.material
			url += "&bullet_1=" + unicode(self.bullet_1, errors="ignore")
			url += "&bullet_2=" + unicode(self.bullet_2, errors="ignore")
			url += "&bullet_3=" + unicode(self.bullet_3, errors="ignore")
			# url += "&currency=" + self.currency
			url += "&price=" + unicode(self.price, errors="ignore")
			url += "&image=" + unicode(self.image, errors="ignore")
			url += "&image_2=" + unicode(self.image_2, errors="ignore")
			url += "&image_3=" + unicode(self.image_3, errors="ignore")

			url += "&id=" + self.identifier

			return urllib.urlopen(url).read()
		else:	

			#color= unicode(color, errors="ignore")
			url += "&category=" + self.category
			url += "&sku=" + self.sku
			url += "&name=" + name
			url += "&upc=" + self.upc
			url += "&description=" + unicode(descripcion, errors="ignore")
			url += "&brand=" + brand
			url += "&manufacturer=" + self.manufacturer
			url += "&size=" + ",".join(str(v) for v in self.size)
			url += "&color=" + color
			#url += "&material=" + self.material
			url += "&bullet_1=" + self.bullet_1
			url += "&bullet_2=" + self.bullet_2
			url += "&bullet_3=" + self.bullet_3
			# url += "&currency=" + self.currency
			url += "&price=" + self.price
			url += "&image=" + self.image
			url += "&image_2=" + self.image_2
			url += "&image_3=" + self.image_3

			url += "&id=" + self.identifier

			return urllib.urlopen(url).read()

	def get_product_list(self):
			
		url = self.wsurl()+"/product/list?token=" + self.token() + "&items=100"
		content = urllib2.urlopen(url).read()

		# parse content to array data
		data = json_util.loads(content)

		self.identifier = data


		return data

	def Search(self, query):
		url = self.wsurl() + "/product/search?token=" + self.token()
		url += "&q=" + query
		# return urllib.urlopen(url).read()

		content = urllib2.urlopen(url).read()

		data = json_util.loads(content)

		self.identifier = data
		
		return data

	# def ProductExist( self, product_sku ):
	# 	url = self.wsurl() + "/product/exists?token=" + self.token()

	# 	url += "&sku=" + product_sku

	# 	json_string = urllib.urlopen( url ).read()
	# 	return json_util.loads( json_string )[ "exists" ]	
