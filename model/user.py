#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2

from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

## TOKEN=5334d6c29ec9a710f56d9ab5

class User(BaseModel):

	def __init__(self):
		self._name = ""
		self._surname = ""
		self._email = ""
		self._password = ""
		self._permissions = ""
		self._identifier = ""


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

	#################
	#### Methods ####
	#################

	def SplitName(self, name):

		try:
			nm = name.split(" ")

			self.name = nm[0]
			self.surname = nm[1]
		except Exception, e:
			raise

	def InitWithEmail(self, email):
		url = self.wsurl() + "/salesman/find"
		url += "?token=" + self.token()
		url += "&email=" + email

		json_string = urllib.urlopen(url).read()

		try:
			data = json_util.loads(json_string)
			self.SplitName(data["nombre"]) ## name and surname
			self.identifier = str(data["_id"])
			self.password = data["password"]
			self.permissions = data["permisos"]
			self.email = data["email"]
		except:
			pass


	def InitWithId(self, idd):
		url = self.wsurl() + "/salesman/find"

		url += "?token=" + self.token()
		url += "&id=" + idd

		json_string = urllib.urlopen(url).read()
		data = json_util.loads(json_string)

		self.SplitName(data["nombre"]) ## name and surname
		self.identifier = str(data["_id"])
		self.password = data["password"]
		self.permissions = data["permisos"]
		self.email = data["email"]

	def Remove(self):
		if self.identifier != "":
			url  =self.wsurl() + "/salesman/delete"
			url += "?token=" + self.token()
			url += "&id=" + self.identifier

			urllib.urlopen(url)

	def Save(self):
		url = self.wsurl() + "/salesman/add?token=" + self.token()

		url += "&nombre=" + self.name + "%20" + self.surname
		url += "&password=" + self.password
		url += "&email=" + self.email
		url += "&permisos=" + self.permissions
		url += "&id=" + self.identifier

		#url = urllib.urlencode(url)
		return urllib.urlopen(url).read()

	def get_users_list(self):

		# getting content from url
		url = self.wsurl() + "/salesman/list?token=" + self.token() + "&items=100"
		content = urllib2.urlopen(url).read()

		# parse content to array data
		data = json_util.loads(content)

		self.identifier = data

		return data
