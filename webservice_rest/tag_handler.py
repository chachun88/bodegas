#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from model10.tag import Tag

from base_handler import BaseHandler
from bson import json_util

class SaveHandler(BaseHandler):

	def get(self):
				
		if not self.ValidateToken():
			return json_util.dumps({"error":"invalid token"})

		name = self.get_argument("name","")
		identifier = self.get_argument("identifier","")

		tag = Tag()

		if name.strip() == "":
			return json_util.dumps({"error":"name is empty"})
		else:
			tag.name = name

		if identifier.strip() != "":
			tag.id = identifier

		response = tag.Save()

		return json_util.dumps(response)

class AddTagProductHandler(BaseHandler):

	def get(self):

		if not self.ValidateToken():
			return json_util.dumps({"error":"invalid token"})

		product_id = self.get_argument("product_id","")
		tag_id = self.get_argument("tag_id","")

		if product_id == "" or tag_id == "":
			return json_util.dumps({"error":"falta product_id o tag_id"})
		else:
			tag = Tag()
			response = tag.AddTagProduct(tag_id,product_id)
			return json_util.dumps(response)

class ListHandler(BaseHandler):

	def get(self):

		page = self.get_argument("page",0)
		items = self.get_argument("items",20)

		tag = Tag()
		res = tag.List(page,items)

		self.write(json_util.dumps(res))

class RemoveHandler(BaseHandler):

	def get(self):

		identificador = self.get_argument("id","")

		if identificador != "":

			tag = Tag()
			eliminar_asociaciones = tag.RemoveTagsAsociationByTagId(identificador)

			if "success" in eliminar_asociaciones:

				eliminar_tag = tag.Remove(identificador)

				self.write(json_util.dumps(eliminar_tag))
				
			else:
				self.write(json_util.dumps(eliminar_asociaciones))

		else:

			self.write(json_util.dumps({"error":"identificador del tag no debe estar vacío"}))

class InitByIdHandler(BaseHandler):

	def get(self):

		identificador = self.get_argument("id","")

		if identificador != "":

			tag = Tag()
			res = tag.InitById(identificador)

			self.write(json_util.dumps(res))

		else:

			self.write(json_util.dumps({"error":"Identificador del tag viene vacío"}))

class GetProductsByTagIdHandler(BaseHandler):

	def get(self):

		identificador = self.get_argument("id","")

		if identificador != "":

			tag = Tag()
			res = tag.GetProductsByTagId(identificador)

			self.write(json_util.dumps(res))

		else:

			self.write(json_util.dumps({"error":"Identificador del tag viene vacío"}))