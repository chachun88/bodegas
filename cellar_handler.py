#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu
from lputils import MoneyFormat

from basehandler import BaseHandler
from model.cellar import Cellar

from bson import json_util

class CellarHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		data = Cellar().List(1, 10)
		self.render("cellar/home.html", MoneyFormat=MoneyFormat,side_menu=self.side_menu, data=data, dn=self.get_argument("dn", ""))


class CellarOutputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/input.html", operation="Salidas", opp="out", side_menu=self.side_menu, cellar=cellar)

	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		redirect = "t"

		if "success" in cellar.RemoveProducts(product_id, units):
			self.write("ok")
			redirect = "bpt"
		else:
			self.write("no")
			redirect = "bpf"

		self.redirect("/cellar?dn=" + redirect)

class CellarInputHandler(BaseHandler):
	def get(self):
		self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

		cellar = Cellar()
		cellar.InitWithId(self.get_argument("id", ""))

		self.render("cellar/input.html",operation="Entradas ", opp="in", side_menu=self.side_menu, cellar=cellar)

	def post(self):
		name = self.get_argument("name", "")
		price = self.get_argument("price", "0")
		units = self.get_argument("units", "0")
		product_id = self.get_argument("product_id", "")
		cellar_id = self.get_argument("cellar_id", "")

		cellar = Cellar()
		cellar.InitWithId(cellar_id)

		redirect = "t"

		if "success" in cellar.AddProducts(product_id, units, price):
			self.write("ok")
			redirect = "bpt"
		else:
			self.write("no")
			redirect = "bpf"

		self.redirect("/cellar?dn=" + redirect)

class CellarDetailHandler(BaseHandler):
	def get(self):

		cellar_id = self.get_argument("cellar_id", "")

		print "entro a detalle "+cellar_id

		self.write("{}".format(cellar_id))

		# cellar = Cellar()
		# cellar.InitWithId(cellar_id)
		self.render("cellar/detail.html", side_menu=self.side_menu)

	def post(self):

		self.redirect("cellar/detail")	