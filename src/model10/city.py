#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
# from bson.objectid import ObjectId

class City(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._name = ''
		self.table = 'City'

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	def List(self):

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

		try:
			cur.execute('''select * from "City"''')
			cities = cur.fetchall()
			return self.ShowSuccessMessage(cities)
		except Exception,e:
			return self.ShowError(str(e))
		finally:
			cur.close()
			self.connection.close()

	def Save(self):

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
		query = '''select id from "City" where lower(name) = lower(%(name)s)'''
		parameters = {
		"name":self.name
		}

		try:
			cur.execute(query,parameters)
			if cur.rowcount > 0:
				self.id = cur.fetchone()["id"]
				# return self.ShowSuccessMessage(self.id)
		except Exception,e:
			return self.ShowError(str(e))
		finally:
			self.connection.close()
			cur.close()

		if self.id != "":

			cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			query = '''update "City" set name = %(name)s where id = %(id)s'''
			parameters = {
			"id":self.id,
			"name":self.name
			}

			try:
				cur.execute(query,parameters)
				self.connection.commit()
				return self.ShowSuccessMessage(self.id)
			except Exception,e:
				return self.ShowError(str(e))
			finally:
				self.connection.close()
				cur.close()

		else:

			cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			query = '''insert into "City" (name) values (%(name)s) returning id'''
			parameters = {
			"name":self.name
			}

			try:
				cur.execute(query,parameters)
				self.id = cur.fetchone()["id"]
				self.connection.commit()
				return self.ShowSuccessMessage(self.id)
			except Exception,e:
				return self.ShowError(str(e))
			finally:
				self.connection.close()
				cur.close()




