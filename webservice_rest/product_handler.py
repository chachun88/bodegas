#!/usr/bin/env python

from model10.product import Product

from base_handler import BaseHandler
from bson import json_util


class AddProductHandler(BaseHandler):
	def get(self):
		
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate product
		product = Product()

		product.category 		= self.get_argument("category", "")
		product.sku 			= self.get_argument("sku", "")
		product.name 			= self.get_argument("name", "")
		product.upc 			= self.get_argument("upc", "")
		product.description 	= self.get_argument("description", "")
		product.brand 			= self.get_argument("brand", "")
		product.manufacturer 	= self.get_argument("manufacturer", "")
		product.size 			= self.get_argument("size", "")
		product.color 			= self.get_argument("color", "")
		product.material 		= self.get_argument("material", "")
		product.bullet_point_1 	= self.get_argument("bullet_1", "")
		product.bullet_point_2 	= self.get_argument("bullet_2", "")
		product.bullet_point_3 	= self.get_argument("bullet_3", "")
		product.price			= self.get_argument("price", "")
		# product.currency 		= self.get_argument("currency", "")
		product.image 			= self.get_argument("image", "")
		product.image_2			= self.get_argument("image_2", "")
		product.image_3 		= self.get_argument("image_3", "")

		# saving current product
		oid = json_util.dumps(product.Save())
		

		self.write(oid)
		

class RemoveProductHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		idd = self.get_argument("id", "")
		sku = self.get_argument("sku", "")

		product = Product()

		if idd != "":
			product.InitById(idd)
		else:
			product.InitBySku(sku)

		self.write(json_util.dumps(product.Remove()))

class GetProductHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return


		idd = self.get_argument("id", "")
		sku = self.get_argument("sku", "")

		product = Product()

		if idd != "":
			product.InitById(idd)
			self.write(json_util.dumps(product.Print()))
		else:
			product.InitBySku(sku)
			self.write(json_util.dumps(product.Print()))


class ListProductsHandler(BaseHandler):
	def get(self):

		#validate access token
		if not self.ValidateToken():
			return
		
		current_page 	= "1"
		items_per_page 	= "10"
		product 		= Product()

		try:
			current_page 	= int(self.TryGetParam("page", "1"))
			items_per_page 	= int(self.TryGetParam("items", "10"))
		except Exception, e:
			print str(e)

		self.write(json_util.dumps(product.GetList(current_page, items_per_page)))

class UploadPictureSampleHandler(BaseHandler):
	def get(self):
		self.render("test_upload.html")
		

class UploadPictureHandler(BaseHandler):
	def get(self):
		pass
	
	def post(self):

		#validate 
		if not self.ValidateToken():
			return

		try:
			image = self.request.files['image'][0]

			output_file = open("uploads/" + image['filename'], 'w')
			output_file.write(image['body'])

			image_number	= self.TryGetParam("number")
			product_id		= self.TryGetParam("id")

			self.finish('se ha subido la imagen')
		except Exception, e:
			self.write(str(e))
			self.finish('se ha producido un error al subir la imagen')
		

class SearchHandler(BaseHandler):
	def get(self):
		query = self.get_argument("q", "")

		product = Product()
		self.write(json_util.dumps(product.Search(query)))
