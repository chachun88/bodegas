#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psycopg2
import psycopg2.extras
import math
from bson import json_util
from bson.objectid import ObjectId

from globals import debugMode, db


class BaseModel(object):
	def __init__(self):
		self._connection = psycopg2.connect("host='ondev.today' dbname='giani' user='yichun' password='chachun88'")
		self._table = ""
		self._id = ""

	@property
	def id(self):
	    return self._id
	@id.setter
	def id(self, value):
	    self._id = value
	
	@property
	def table(self):
	    return self._table
	@table.setter
	def table(self, value):
	    self._table = value
	

	@property
	def connection(self):
	    return self._connection
	
	def Save(self):
		return ShowError("must be overriden by user")

	def InitById(self, idd):
		return ShowError("must be overriden by user")

	def GetList(self, page, items):

		page = int(page)
		items = int(items)
		offset = (page-1)*items
		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		try:
			cur.execute("select from \"{tabla}\" limit {items} offset {offset}".format(tabla=self.table,items=items,offset=offset))
			lista = cur.fetchall()
			return lista
		except Exception,e:
			print str(e)
			return {}

		# return self.collection.find().skip((page-1)*items).limit(items)

	#@return integer
	def GetPages(self, limit):

		items = float(limit)
		cur = self.connection.cursor()
		try:
			cur.execute("select count(*) from \"{tabla}\"".format(tabla=self.table))
			total = float(cur.fetchone()[0])
			paginas = math.floor(total/items)
			return paginas
		except Exception,e:
			print str(e)
			return 0

		# try:
		# 	items = int(limit)
		# 	items = self.collection.find().count() / items

		# 	return items
		# except Exception, e:
		# 	return 0

	#@return json object
	def Remove(self):
		try:
			## raise exception if identifier is empty
			if self.id == "":
				raise

			cur = self.connection.cursor()
			cur.execute("delete from \"{tabla}\" where id = {id}".format(tabla=self.table,id=self.id))

			return self.ShowSuccessMessage("object: " + self.id + " has been deleted")
		except Exception, e:
			return self.ShowError("object: not found")

	#@return json object
	def ShowError(self, error_text):
		return {'error': error_text}

	#@return json object
	def ShowSuccessMessage(self, message):
		return {'success': message}
