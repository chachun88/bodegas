#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler

DEFAULT_IMAGE = "static/default_image.png"

class ImageHandler(BaseHandler):

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

	def get(self):
		self.set_header('Content-Type', 'image/png')
		img = open(DEFAULT_IMAGE, 'r')
		self.write(img.read())
		self.finish()
		