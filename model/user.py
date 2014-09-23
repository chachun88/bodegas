#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2

#from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

## TOKEN=5334d6c29ec9a710f56d9ab5

class User(BaseModel):

	def __init__(self):
		BaseModel.__init__(self)
		self._name = ""
		self._surname = ""
		self._email = ""
		self._password = ""
		self._permissions = ""
		self._identifier = ""
		self._salesman_id = ""
		self._cellars = []


	####################
	### Class fields ###
	####################

	@property
	def salesman_id(self):
	    return self._salesman_id
	@salesman_id.setter
	def salesman_id(self, value):
	    self._salesman_id = value
	

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

	@property
	def surname(self):
	    return self._surname
	@surname.setter
	def surname(self, value):
	    self._surname = value
	
	@property
	def email(self):
	    return self._email
	@email.setter
	def email(self, value):
	    self._email = value
	
	@property
	def password(self):
	    return self._password
	@password.setter
	def password(self, value):
	    self._password = value
	
	@property
	def permissions(self):
	    return self._permissions
	@permissions.setter
	def permissions(self, value):
	    self._permissions = value

	@property
	def cellars(self):
	    return self._cellars
	@cellars.setter
	def cellars(self, value):
	    self._cellars = value

	@property
	def permissions_name(self):
	    return self._permissions_name
	@permissions_name.setter
	def permissions_name(self, value):
	    self._permissions_name = value
	
	@property
	def cellars_name(self):
	    return self._cellars_name
	@cellars_name.setter
	def cellars_name(self, value):
	    self._cellars_name = value
	
	

	#################
	#### Methods ####
	#################

	# def SplitName(self, name):

	# 	try:
	# 		nm = name.split(" ")

	# 		self.name = nm[0]

	# 		if len(nm) > 1:
	# 			self.surname = nm[1]
	# 	except Exception, e:
	# 		raise

	def InitWithEmail(self, email):
		url = self.wsurl() + "/salesman/find"
		url += "?token=" + self.token
		url += "&email=" + email

		json_string = urllib.urlopen(url).read()

		try:
			return json_string
		except:
			return {}
			pass


	def InitWithId(self, idd):
		url = self.wsurl() + "/salesman/find"

		url += "?token=" + self.token
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.name = data["name"]
		self.surname = data["lastname"]
		self.identifier = idd
		self.password = data["password"]
		self.permissions = data["permissions"]
		self.email = data["email"]
		# self.salesman_id = data["salesman_id"]
		self.cellars = data["cellar_permissions"]
		self.cellars_name = data["cellars_name"]
		self.permissions_name = data["permissions_name"]

	def Remove(self):

		if self.identifier != "":
			url  =self.wsurl() + "/salesman/delete"
			url += "?token=" + self.token
			url += "&id=" + self.identifier

			response = urllib.urlopen(url).read()

			print response

			# print "url : {}".format( url )

	def Save(self):
		url = self.wsurl() + "/salesman/add?token=" + self.token

		url += "&name=" + self.name 
		url += "&lastname=" + self.surname
		url += "&password=" + self.password
		url += "&email=" + self.email


		if type(self.permissions) == list:
			url += "&permissions=" + urllib.quote ( ",".join(self.permissions).encode("utf8") )
		else:
			url += "&permissions=" + urllib.quote ( self.permissions.encode("utf8") )
		

		if type(self.cellars) == list:
			url += "&cellars=" + urllib.quote ( ",".join(self.cellars).encode("utf8") )
		else:
			url += "&cellars=" + urllib.quote ( self.cellars.encode("utf8") )
		url += "&id=" + self.identifier

		#url = urllib.urlencode(url)
		return urllib.urlopen(url).read()

	def get_users_list(self):

		# getting content from url
		url = self.wsurl() + "/salesman/list?token=" + self.token + "&items=100"
		content = urllib2.urlopen(url).read()

		# parse content to array data
		data = json_util.loads(content)

		self.identifier = data

		return data
