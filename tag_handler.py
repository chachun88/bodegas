#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler

from bson import json_util

from model.tag import Tag
from model.product import Product

class TagHandler(BaseHandler):

	def get(self):

		page = self.get_argument("page",1)
		items = self.get_argument("items",20)

		tag = Tag()
		res = tag.List(page,items)

		if "success" in res:
			self.render("tag/list.html",lista=res["success"],dn="")
		else:
			self.render("tag/list.html",dn="error",mensaje=res["error"])

class RemoveHandler(BaseHandler):

	def get(self):

		identificador = self.get_argument("id","")

		if identificador != "":

			tag = Tag()
			res = tag.Remove(identificador)

			if "success" in res:
				self.redirect("/tags")
			else:
				self.write(res["error"])
		else:
			self.write("identificador del tag está vacío")

class HideShowHandler(BaseHandler):

	def get(self):

		identificador = self.get_argument("id","")
		tipo = self.get_argument("type","")

		if identificador != "" and tipo != "":
			
			tag = Tag()
			res = tag.HideShow(identificador,tipo)

			if "success" in res:
				self.redirect("/tags")
			else:
				self.write(res["error"])
		else:
			self.write("identificador del tag está vacío y/o operación no está definida")

class EditHandler(BaseHandler):

	def get(self):

		identifier = self.get_argument("id","")

		if identifier != "":
			
			tag = Tag()
			res = tag.InitById(identifier)

			productos_asociados = tag.GetProductsByTagId(identifier)

			if "success" in productos_asociados:

				asociados = productos_asociados["success"]

				if "success" in res:
					product = Product()
					lista = product.get_product_list()
					self.render("tag/save.html",tag=tag,mode="edit",product_list=lista,dn="",asociados=asociados)
				else:
					self.write(res["error"])

			else:
				self.write(res["error"])
		else:
			self.write("identificador del tag está vacío")

