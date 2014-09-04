#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel, db

class SalesmanPermission(BaseModel):
	def __init__(self):
		BaseModel.__init__(self)
		self._salesman_identifier = ''
		self._permission_identifier = ''

		self.collection = db.salesman_permissions

	@property
	def salesman_identifier(self):
		return self._salesman_identifier
	@salesman_identifier.setter
	def salesman_identifier(self, value):
		self._salesman_identifier = value 

	@property
	def permission_identifier(self):
		return self._permission_identifier
	@permission_identifier.setter
	def permission_identifier(self, value):
		self._permission_identifier = value


	def RemoveAllByUser(self):
		# try:
		# 	self.collection.remove({
		# 		"salesman_identifier":self.salesman_identifier
		# 		})
		# 	return self.ShowSuccessMessage("all permissions deleted")
		# except:
		# 	return self.ShowError("an error ocurred")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:
			q = '''update "User" set permissions = Array[] where id = %(id)s'''
			p = {"id":self.salesman_identifier}
			cur.execute(q,p)
			self.connection.commit()
			return self.ShowSuccessMessage("all permissions deleted")
		except Exception,e:
			return self.ShowError("an error ocurred, error:{}".format(str(e)))

	def RemovePermission(self):
		# try:
		# 	self.collection.remove({
		# 							"salesman_identifier" : self.salesman_identifier,
		# 							"permission_identifier" : self.permission_identifier
		# 							})

		# 	return self.ShowSuccessMessage("permission deleted")
		# except:
		# 	return self.ShowError("permission cant be deleted")

		cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

		try:
			q = '''update "User" set permissions = Array[] where id = %(id)s'''
			p = {"id":self.salesman_identifier}
			cur.execute(q,p)
			self.connection.commit()
			return self.ShowSuccessMessage("all permissions deleted")
		except Exception,e:
			return self.ShowError("permission cant be deleted, erro:{}".format(str(e)))

	def Save(self):
		try:
			# validate identifier
			data = self.collection.find({
										"salesman_identifier" : self.salesman_identifier,
										"permission_identifier" : self.permission_identifier
										})
			if data.count() >= 1:

				self.identifier = self.collection.update(
					{"_id" : data[0]["_id"]},
					{"$set" : {
						"salesman_identifier" : self.salesman_identifier,
						"permission_identifier" : self.permission_identifier
					}})

				return self.ShowSuccessMessage(self.permission_identifier)

			#save the object and return the id
			object_id = self.collection.insert(
				{
				"salesman_identifier" : self.salesman_identifier,
				"permission_identifier" : self.permission_identifier
				})

			self.identifier = object_id

			return self.ShowSuccessMessage(self.permission_identifier)
		except Exception, e:
			print "aa:" + str(e)
			return self.ShowError("failed to save permission " + self.permission_identifier)

	def FindPermissions(self, sales_man_id):
		permission_list = []
		data = self.collection.find({"salesman_identifier":sales_man_id})

		for permission in data:
			permission_list.append(permission["permission_identifier"])

		return permission_list
