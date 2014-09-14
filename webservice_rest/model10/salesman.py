#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db
from salesmanpermission import SalesmanPermission
# from bson.objectid import ObjectId
import psycopg2
import psycopg2.extras


class Salesman(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		# self.collection = db.salesman
		self.table = 'User'
		self._salesman_id = ''
		self._name = ''
		self._password = '' 
		self._email = ''
		self._permissions = []
		self._cellars = []
		self._permissions_name = []
		self._cellars_name = []

	@property
	def salesman_id(self):
	    return self._salesman_id
	@salesman_id.setter
	def salesman_id(self, value):
	    self._salesman_id = value
	

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def password(self):
		return self._password
	@password.setter
	def password(self, value):
		self._password = value

	@property
	def email(self):
		return self._email
	@email.setter
	def email(self, value):
		self._email = value

	@property
	def permissions(self):
	    return self._permissions
	@permissions.setter
	def permissions(self, value):
	    self._permissions = value

	@property
	def user_type(self):
	    return self._user_type
	@user_type.setter
	def user_type(self, value):
	    self._user_type = value
	
	@property
	def permissions_name(self):
	    return self._permissions_name
	@permissions_name.setter
	def permissions_name(self, value):
	    self._permissions_name = value

	@property
	def cellars(self):
	    return self._cellars
	@cellars.setter
	def cellars(self, value):
	    self._cellars = value

	@property
	def cellars_name(self):
	    return self._cellars_name
	@cellars_name.setter
	def cellars_name(self, value):
	    self._cellars_name = value
	
	
	

	def Print(self):
		return {
			"id":self.id,
			"name":self.name,
			"email":self.email,
			"password":self.password,
			"permissions":self.permissions,
			"salesman_id":self.salesman_id,
			"permissions_name":self.permissions_name,
			"cellars":self.cellars,
			"cellars_name":self.cellars_name
		}

	def Remove(self):
		try:
			#delete = self._permissions.RemoveAllByUser()
			#if "error" in delete:
			#	return delete

			return BaseModel.Remove(self)
		except Exception, e:
			return self.ShowError("error removing user")

	def Login(self, username, password):
		# data = self.collection.find({"email":username, "password":password})

		# if data.count() >= 1:
		# 	self.InitByEmail(username) ## init user
		# 	return True
		# return False

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		q = '''select count(1) from "User" where email = %(email)s and %(password)s limit 1'''
		p = {
		"email":username,
		"password":password
		}
		try:
			cur.execute(q,p)
			existe = cur.fetchone()
			if existe:
				return True
			else:
				return False
		except:
			return False

	def InitByEmail(self, email):

		# try:
		# 	data = self.collection.find({"email":email})
		# 	if data.count() >= 1:
		# 		self.name 		= data[0]["name"]
		# 		self.password 	= data[0]["password"]
		# 		self.email 		= email
		# 		self.identifier = str(data[0]["_id"])
		# 		self.permissions= data[0]["permissions"]
		# 		self.id         = data[0]["salesman_id"]

		# 		return self.ShowSuccessMessage("user initialized")
		# 	else:
		# 		raise
		# except Exception, e:
		# 	return self.ShowError("user : " + email + " not found")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		q = '''select u.*, STRING_AGG(distinct p.name, ',') as permissions_name, STRING_AGG(distinct c.name, ',') as cellars_name from "User" u left join "Permission" p on p.id = any(u.permissions) left join "Cellar" c on c.id = any(u.cellar_permissions) where u.email = %(email)s group by u.id limit 1'''
		p = {
		"email":email
		}
		try:
			cur.execute(q,p)
			usuario = cur.fetchone()
			if usuario:
				return usuario
			else:
				return self.ShowError("user : " + email + " not found")
		except:
			return self.ShowError("user : " + email + " not found")

	def InitById(self, idd):

		# try:
		# 	data = self.collection.find({"_id":ObjectId(idd)})
		# 	if data.count() >= 1:
		# 		self.name 		= data[0]["name"]
		# 		self.password 	= data[0]["password"]
		# 		self.email 		= data[0]["email"]
		# 		self.identifier = str(data[0]["_id"])
		# 		self.permissions=  data[0]["permissions"]
		# 		self.id         = data[0]["salesman_id"]

		# 		return self.ShowSuccessMessage("user initialized")
		# 	else:
		# 		raise
		# except Exception, e:
		# 	return self.ShowError("user : " + idd + " not found")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		q = '''select u.*, STRING_AGG(distinct p.name, ',') as permissions_name, STRING_AGG(distinct c.name, ',') as cellars_name from "User" u left join "Permission" p on p.id = any(u.permissions) left join "Cellar" c on c.id = any(u.cellar_permissions) where u.id = %(id)s group by u.id limit 1'''
		p = {
		"id":idd
		}
		try:
			cur.execute(q,p)
			usuario = cur.fetchone()
			if usuario:
				return usuario
			else:
				return self.ShowError("user : " + idd + " not found")
		except:
			return self.ShowError("user : " + idd + " not found")

	def GetPermissions(self):
		return self._permissions.FindPermissions(self.id)


	def AssignPermission(self, permission):
		## TODO: validate if permission exist
		self._permissions.salesman_id 	= self.id
		self._permissions.permission_id = permission
		return self._permissions.Save()


	def RemovePermission(self, permission):
		self._permissions.salesman_id = self.id
		self._permissions.permission_id = permission
		return self._permissions.RemovePermission()

	def Save(self):
		# try:
		# 	# validate identifier
		# 	data = self.collection.find({"email" : self.email})

		# 	new_id = db.seq.find_and_modify(query={'seq_name':'salesman_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True)["id"]

		# 	if data.count() >= 1:

		# 		self.identifier = str(self.collection.update(
		# 			{"_id" : data[0]["_id"]},
		# 			{"$set" : {
		# 				"name" 		: self.name,
		# 				"password"  : self.password,
		# 				"email" 	: self.email,
		# 				"permissions": self.permissions
		# 			}}))

		# 		return self.ShowSuccessMessage(str(data[0]["_id"]))

		# 	#save the object and return the id
		# 	object_id = self.collection.insert(
		# 		{
		# 		"salesman_id": new_id,
		# 		"name" 		: self.name,
		# 		"password"  : self.password,
		# 		"email"  	: self.email,
		# 		"permissions": self.permissions
		# 		})

		# 	self.identifier = str(object_id)

		# 	return self.ShowSuccessMessage(str(object_id))
		# except Exception, e:
		# 	return self.ShowError("failed to save user " + self.email)

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		q = '''select id from "Permission" where name = any(%(permissions)s)'''
		p = {
		"permissions":self.permissions
		}
		cur.execute(q,p)
		permisos = cur.fetchall()

		q = '''select id from "User_Types" where name = %(name)s'''
		p = {
		"name":"Vendedor"
		}
		cur.execute(q,p)
		tipo_usuario = cur.fetchone()[0]

		q = '''select * from "User" where email = %(email)s limit 1'''
		p = {
		"email":self.email
		}
		cur.execute(q,p)
		usuario = cur.fetchone()

		try:

			if cur.rowcount > 0:
				self.id = usuario['id']
				q = '''update "User" set name = %(name)s, password = %(password)s, email = %(email)s, permissions = %(permissions)s, type_id = %(type_id)s where id = %(id)s'''
				p = {
				"name":self.name,
				"email":self.email,
				"permissions":permisos,
				"password":self.password,
				"id":self.id,
				"type_id":tipo_usuario
				}
				cur.execute(q,p)
				self.connection.commit()
				return self.ShowSuccessMessage(str(self.id))
			else:
				q = '''insert into "User" (name,password,email,permissions,type_id) values (%(name)s,%(password)s,%(email)s,%(permissions)s,%(type_id)s) returning id'''
				p = {
				"name":self.name,
				"email":self.email,
				"permissions":permisos,
				"password":self.password,
				"type_id":tipo_usuario
				}
				cur.execute(q,p)
				self.connection.commit()
				self.id = cur.fetchone()[0]

				return self.ShowSuccessMessage(str(self.id))
		except Exception,e:
			return self.ShowError("failed to save user {}, error:{}".format(self.email,str(e)))

	def GetList(self, page, items):

		page = int(page)
		items = int(items)
		offset = (page-1)*items
		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		try:
			q = '''select u.*, STRING_AGG(distinct p.name, ',') as permissions_name, STRING_AGG(distinct c.name, ',') as cellars_name from "User" u left join "Permission" p on p.id = any(u.permissions) left join "Cellar" c on c.id = any(u.cellar_permissions) group by u.id limit %(limit)s offset %(offset)s'''
			p = {
			"limit":items,
			"offset":offset
			}
			cur.execute(q,p)

			lista = cur.fetchall()
			return lista
		except Exception,e:
			print str(e)
			return {}
