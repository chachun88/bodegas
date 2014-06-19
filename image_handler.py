#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os

from basehandler import BaseHandler

DEFAULT_IMAGE = "static/default_image.png"

class ImageHandler(BaseHandler):

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self, image_name):
		self.set_header('Content-Type', 'image/png')

		try:
			img = open('uploads/images/' + image_name, 'r')
			self.write(img.read())
			self.finish()
		except:
			img = open(DEFAULT_IMAGE, 'r')
			self.write(img.read())
			self.finish()

class ImageHandler2(BaseHandler):

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		self.set_header('Content-Type', 'image/png')
		img = open(DEFAULT_IMAGE, 'r')
		self.write(img.read())
		self.finish()
		

class ImageDeleteHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		try:

			image_name = self.get_argument("image_name", "")
			if image_name != "":
				os.remove( 'uploads/images/' + image_name )
		except:
			pass

		self.write("imagen eliminada")