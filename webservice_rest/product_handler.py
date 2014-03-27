#!/usr/bin/env python

from model.product import Product

from base_handler import BaseHandler

class AddProductHandler(BaseHandler):
	def get(self):
		
		# validate access token
		if not self.ValidateToken():
			return

		# isntantitate product
		product = Product()

		product.codigo_proveedor = self.TryGetParam("codigo_proveedor", "")
		product.codigo_interno = self.TryGetParam("codigo_interno", "")
		product.nombre = self.TryGetParam("nombre", "")
		product.precio = self.TryGetParam("precio", "")
		product.stock = self.TryGetParam("stock", "")
		product.descuento = self.TryGetParam("descuento", "")
		product.estado = self.TryGetParam("estado", "")
		product.marca = self.TryGetParam("marca", "")
		product.familia = self.TryGetParam("familia", "")
		product.descripcion = self.TryGetParam("descripcion", "")

		# saving current product
		oid = product.Save(self.db.products)
		

		self.write(oid)
		

class RemoveProductHandler(BaseHandler):
	def get(self):
		# validate access token
		if not self.ValidateToken():
			return

		product = Product()
		product.RemoveById(self.TryGetParam("id", ""), self.db.products)

class GetProductHandler(BaseHandler):
	def get(self):

		# validate access token
		if not self.ValidateToken():
			return

		product = Product()
		self.write(product.FindById(self.TryGetParam("id", ""), self.db.products))

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
		
		self.write(product.GetList(current_page, items_per_page, self.db.products))
		

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
		
		
