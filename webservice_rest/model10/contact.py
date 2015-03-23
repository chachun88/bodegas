#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from basemodel import BaseModel
import psycopg2
import psycopg2.extras

class Contact(BaseModel):

	@property
	def id(self):
		return self._id
	@id.setter
	def id(self, value):
		self._id = value

	@property
	def user_id(self):
		return self._user_id
	@user_id.setter
	def user_id(self, value):
		self._user_id = value

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value
	
	@property
	def type_id(self):
		return self._type_id
	@type_id.setter
	def type_id(self, value):
		self._type_id = value
	
	@property
	def address(self):
		return self._address
	@address.setter
	def address(self, value):
		self._address = value
	
	@property
	def telephone(self):
		return self._telephone
	@telephone.setter
	def telephone(self, value):
		self._telephone = value
	
	@property
	def email(self):
		return self._email
	@email.setter
	def email(self, value):
		self._email = value

	@property
	def type(self):
	    return self._type
	@type.setter
	def type(self, value):
	    self._type = value
	

	def __init__(self):
		BaseModel.__init__(self)
		self._id = ""
		self._name = ""
		self._type_id = ""
		self._telephone = ""
		self._email = ""
		self._address = ""
		self._user_id = ""
		self._type = ""
		self._lastname = ""
		self._city = ""
		self._zip_code = ""
		self._additional_info = ""
		self._town = ""
		self._rut = ""

	def InitById(self, _id):

		# contact = self.collection.find_one({"id":int(_id)})

		# if contact:
		# 	return contact
		# else:
		# 	return ""

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		query = '''select c.id, c.user_id, c.name, c.city_id, c.email, c.address, c.telephone, c.zip_code, c.lastname, c.additional_info, c.lastname, c.town, c.rut, ct.name as type, city.name as city from "Contact" c 
		inner join "Contact_Types" ct on ct.id = c.type_id 
		inner join "City" city on city.id = c.city_id
		where c.id = %(id)s limit 1'''

		parametros = {
		"id":_id
		}

		try:
			cur.execute(query,parametros)
			contact = cur.fetchone()
			return contact
		except:
			return ""

	def Save(self):

		#new_id = db.seq.find_and_modify(query={'seq_name':'contact_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

		contact = {
		"name": self.name,
		"type_id": self.type_id,
		"telephone": self.telephone,
		"email": self.email,
		"user_id": self.user_id,
		"address": self.address,
		"lastname": self.lastname,
		"city_id": self.city,
		"zip_code": self.zip_code,
		"additional_info":self.additional_info,
		"town":self.town,
		"rut":self.rut
		}

		try:

			# self.collection.insert(contact)
			cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
			query = '''insert into "Contact" (name,type_id,telephone,email,user_id,address, lastname, city_id, zip_code,additional_info,town,rut)
			values (%(name)s,%(type_id)s,%(telephone)s,%(email)s,%(user_id)s,%(address)s,%(lastname)s,%(city_id)s,%(zip_code)s,%(additional_info)s,%(town)s,%(rut)s) returning id'''
			print cur.mogrify(query,contact)
			cur.execute(query,contact)
			self.connection.commit()
			new_id = cur.fetchone()[0]
			return self.ShowSuccessMessage("{}".format(new_id))

		except Exception, e:

			return self.ShowError(str(e))

	def Edit(self):

		print "Edit WS id:{}\n".format(self.id)

		contact = {
		"name": self.name,
		"type_id": self.type_id,
		"telephone": self.telephone,
		"email": self.email,
		"user_id": self.user_id,
		"address":self.address,
		"id":self.id,
		"city_id":self.city,
		"zip_code":self.zip_code,
		"lastname":self.lastname,
		"additional_info":self.additional_info,
		"town":self.town,
		"rut":self.rut
		}

		# try:
		# 	self.collection.update({"id":int(self.id)},{"$set":contact})
		# 	return self.id
		# except Exception, e:

		# 	return str(e)

		try:

			# self.collection.insert(contact)
			cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
			query = '''update "Contact" set 
										name = %(name)s, 
										type_id = %(type_id)s, 
										telephone = %(telephone)s, 
										email = %(email)s, 
										user_id = %(user_id)s, 
										address = %(address)s, 
										lastname = %(lastname)s,
										zip_code = %(zip_code)s,
										additional_info = %(additional_info)s,
										town = %(town)s,
										city_id = %(city_id)s,
										rut = %(rut)s
						where id = %(id)s'''
			cur.execute(query,contact)
			self.connection.commit()
			
			return self.ShowSuccessMessage(self.id)

		except Exception, e:

			return self.ShowError(str(e))

	def ListByCustomerId(self, _user_id):

		# contacts = self.collection.find({"user_id":_user_id})

		# if contacts:
		# 	return contacts
		# else:
		# 	return []

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:

			query = '''select c.id,
			c.user_id,
			c.city_id,
			c.name,
			c.email,
			c.address,
			c.telephone,
			c.zip_code,
			c.lastname,
			c.additional_info,
			c.lastname,
			c.town,
			c.rut,
			ct.name as type, 
			city.name as city 
			from "Contact" c 
			inner join "Contact_Types" ct on ct.id = c.type_id 
			inner join "City" city on city.id = c.city_id
			inner join "User" user on u.id = c.user_id 
			where c.user_id = %(user_id)s'''
			
			parametros = {
			"user_id":_user_id
			}
			cur.execute(query,parametros)
			contactos = cur.fetchall()

			return self.ShowSuccessMessage(contactos)
			
		except Exception,e:

			return self.ShowError(str(e))

	def Remove(self,ids):
		print ids
		# self.collection.remove({"id":{"$in":[int(n) for n in ids.split(",")]}})

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		query = '''delete from "Contact" where id = ANY(%(id)s)'''

		parametros = {
		"id":[int(n) for n in ids.split(",")]
		}

		try:
			cur.execute(query,parametros)
			self.connection.commit()
			return self.ShowSuccessMessage("ok")
		except Exception,e:
			return self.ShowError(str(e))

	def GetTypes(self):

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		query = '''select * from "Contact_Types"'''

		try:
			cur.execute(query)
			tipos = cur.fetchall()
			return self.ShowSuccessMessage(tipos)
		except Exception,e:
			return self.ShowError(str(e))