 #!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import pymongo

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import xlrd #lib excel
import os
import commands
import cgi, cgitb
import cgi, os
import cgitb; cgitb.enable()
import sys

from tornado.options import define, options

from basehandler import BaseHandler
from model.product import Product
from model.cellar import Cellar
from globals import port, debugMode, carpeta_img, userMode, Menu

class HomeHandler(BaseHandler):

	fn =''
	fnout =''

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def get(self):
		self.set_active(Menu.PRODUCTOS_CARGA_MASIVA) #change menu active item

		dn = self.get_argument("dn", "f")
		w = []

		if self.get_argument("w", "") != "":
			w = self.get_argument("w", "").split( "," )

		self.render("product/home.html", side_menu=self.side_menu, dn=dn, w=w)

	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):
		
		#upload file 
		try: # Windows needs stdio set for binary mode.
		    import msvcrt
		    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
		except ImportError:
		    pass

		  
		form = cgi.FieldStorage()
		
		fileitem=''
		# A nested FieldStorage instance holds the file
		try:
			fileitem = self.request.files['file'][0]
		except:
			pass
	
		# strip leading path from file name to avoid directory traversal attacks		

		if fileitem != "":
			global fn 
			
			fn = fileitem['filename']
			open('uploads/entradas_masivas/' + fn, 'wb').write(fileitem["body"])
			#message = 'The file "' + fn + '" was uploaded successfully'

			if os.name == "nt":

				try:
					#dn = self.get_argument("dn", "t")
					dn="t"
				
					doc = xlrd.open_workbook('uploads/entradas_masivas/'+fn)

					sheet = doc.sheet_by_index(0)

					nrows = sheet.nrows
					ncols = sheet.ncols
					#print ncols
					#self.write("{}".format(ncols))

					matriz=[]

					for i in range(nrows):
						matriz.append([])
						for j in range(ncols):
							matriz[i].append(sheet.cell_value(i,j))	

					#self.redirect("/product?dn="+dn+"&matriz="+matriz+"&nrows="+nrows+"&ncols="+ncols)
					self.render("product/home.html", side_menu=self.side_menu, matriz=matriz, nrows=nrows, ncols=ncols, dn="", w="")

				except ImportError:
					pass
			else:
				try:
					#dn = self.get_argument("dn", "t")
					dn="t"
				
					doc = xlrd.open_workbook('uploads/entradas_masivas/'+fn)

					sheet = doc.sheet_by_index(0)

					nrows = sheet.nrows
					ncols = sheet.ncols
					#print ncols
					#self.write("{}".format(ncols))

					matriz=[]

					for i in range(nrows):
						matriz.append([])
						for j in range(ncols):
							matriz[i].append(sheet.cell_value(i,j))	

					#self.redirect("/product?dn="+dn+"&matriz="+matriz+"&nrows="+nrows+"&ncols="+ncols)
					self.render("product/home.html", side_menu=self.side_menu, matriz=matriz, nrows=nrows, ncols=ncols, dn="",  w="")

				except ImportError:
					pass	

		else:
			dn="t2"
			self.render("product/home.html", side_menu=self.side_menu, dn=dn, w="")




class ProductLoadHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		pass

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):	

		warnings = []

		if 'fn' in vars() or 'fn' in globals():

			if fn != "":

				doc = xlrd.open_workbook('uploads/entradas_masivas/'+fn)

				sheet = doc.sheet_by_index(0)

				nrows = sheet.nrows
				ncols = sheet.ncols
				#print ncols
				#self.write("{}".format(ncols))

				matriz=[]
				tallas=[]

				prod = Product()
				cellar=Cellar()

				for i in range(nrows):	
					matriz.append([])
					for j in range(ncols):				
						if i == 3 and j > 9:
							tallas.append(sheet.cell_value(i,j))				

				try:			
					for i in range(nrows):	
						matriz.append([])
						for k in range(len(tallas)):
							for j in range(ncols):

								matriz[i].append(sheet.cell_value(i,j))
								
								try: 
									if i > 3 and i < nrows:
										prod.size=str(tallas[k]).split(",")
										size=str(tallas[k])
										if j == 0:
											prod.category = matriz[i][j].encode('utf-8')
										elif j == 1:
											prod.sku = str(matriz[i][j]).encode('utf-8')
										elif j == 2:
											prod.name = matriz[i][j].encode('utf-8')
										elif j == 3:
											prod.description = matriz[i][j].encode('utf-8')
										elif j == 4:										
											prod.color=matriz[i][j].encode('utf-8')
											color=matriz[i][j].encode('utf-8')
										elif j == 5:
											price = matriz[i][j]
											prod.price = str(price).strip()
										elif j == 6:
											prod.manufacturer = matriz[i][j].encode('utf-8')
										elif j == 7:
											cellar_name= matriz[i][j].encode('utf-8')
										elif j == 8:
											prod.brand = matriz[i][j].encode('utf-8')
										elif j == 10:
											try:
												q = k +j

												quantity=str(matriz[i][q])
				

												try:
													prod.Save("masive")
												except Exception, e:
													print "prod.Save('masive'): {}".format(str(e))

												operation="buy"

												#products stored for cellar
												if cellar.CellarExist( cellar_name ):
													cellar.InitWithName(cellar_name)

													try:
														cellar.AddProducts(prod.sku, quantity, price, size, color, operation, self.get_user_email() )
													except Exception, e:
														print "cellar.AddProducts: {}".format(str(e))
														
												else:
													error_name = "No existe la bodega \"" + cellar_name + "\""
													if error_name not in warnings:
														warnings.append( error_name )
											except Exception, e:
												print "se cae al guardar, error:{}".format(str(e))
												pass	

								except Exception, e:
									print "Error:{}".format(str(e))
									dn="t3"
									self.redirect("/product?dn="+dn + "&w=" + ",".join(warnings))
									return
				except Exception, e:
					print "fiiiiiiinnnnnnn "+str(j)+" "+str(e)			#product is stored


				dn="t"
				#self.redirect("/product?dn="+dn)
				#self.render("product/home.html", side_menu=self.side_menu, dn=dn)


			else:
				dn="t2"
		else:
			dn="t2"
		

		self.redirect("/product?dn="+dn + "&w=" + ",".join(warnings))

class ProductRemoveHandler(BaseHandler):
	
	@tornado.web.authenticated
	def get(self):

		prod = Product()
		prod.InitWithId(self.get_argument("id", ""))

		cellar_id="remove"
		size="remove"

		cellar = Cellar()		
		product_find =cellar.ProductKardex(prod.sku, cellar_id, size)



		buy=0
		sell=0

		for p in product_find:
			if p["operation_type"] == "buy":
				buy=p["total"]	

			if p["operation_type"] == "sell":
				sell=p["total"]

		units=buy-sell	

		if units > 0:
			self.render("product/list.html", dn="bpf", side_menu=self.side_menu, product_list=prod.get_product_list())	
		else:
			
			prod.Remove()	

			self.render("product/list.html", dn="bpt", side_menu=self.side_menu, product_list=prod.get_product_list())
			#self.redirect("/product/list")

class ProductOutHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		self.set_active(Menu.PRODUCTOS_SALIDA_MASIVA) #change menu active item

		dn = self.get_argument("dn", "f")

		self.render("product/out.html", side_menu=self.side_menu, dn=dn)

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):

		#upload file 
		try: # Windows needs stdio set for binary mode.
		    import msvcrt
		    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
		    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
		except ImportError:
		    pass

		  
		form = cgi.FieldStorage()
		
		fileitem=''
		try:
			# A nested FieldStorage instance holds the file
			fileitem = self.request.files['file'][0]
		except:
			pass
	
		# strip leading path from file name to avoid directory traversal attacks

		
		if fileitem != "":

			global fnout 

			fnout = fileitem['filename']

			dir = "uploads/salidas_masivas/"

			## chegk if directory exists
			try:
				os.stat( dir )
			except:
				os.mkdir(dir)

			open('uploads/salidas_masivas/' + fnout, 'wb').write(fileitem["body"])
			#message = 'The file "' + fn + '" was uploaded successfully'

			try:
				dn = self.get_argument("dn", "f")
			
				doc = xlrd.open_workbook('uploads/salidas_masivas/'+fnout)

				sheet = doc.sheet_by_index(0)

				nrows = sheet.nrows
				ncols = sheet.ncols
				#print ncols
				#self.write("{}".format(ncols))

				matriz=[]

				for i in range(nrows):
					matriz.append([])
					for j in range(ncols):
						matriz[i].append(sheet.cell_value(i,j))

				self.render("product/out.html", side_menu=self.side_menu, dn=dn, matriz=matriz, nrows=nrows, ncols=ncols)

			except ImportError:
				pass
		else:
			dn="t2"
			self.render("product/out.html", side_menu=self.side_menu, dn=dn)

class ProductMassiveOutputHandler(BaseHandler):

	@tornado.web.authenticated
	def get(self):
		pass

	@tornado.web.authenticated
	@tornado.web.asynchronous
	@tornado.gen.engine
	def post(self):

		if 'fnout' in vars() or 'fnout' in globals():

			if fnout != "":

				doc = xlrd.open_workbook('uploads/salidas_masivas/'+fnout)

				sheet = doc.sheet_by_index(0)

				nrows = sheet.nrows
				ncols = sheet.ncols
				#self.write("{}".format(ncols))

				matriz=[]
				tallas=[]

				prod = Product()
				cellar=Cellar()

				for i in range(nrows):	
					matriz.append([])
					for j in range(ncols):				
						if i == 3 and j > 11:
							tallas.append(sheet.cell_value(i,j))				

				for i in range(nrows):	
					matriz.append([])
					for k in range(len(tallas)):
						for j in range(ncols):	

							matriz[i].append(sheet.cell_value(i,j))
							
							# try: 
							if i > 3 and i < nrows:
								prod.size=str(tallas[k]).split(",")
								size=str(tallas[k])
								if j == 0:
									prod.category = matriz[i][j].encode('utf-8')
								elif j == 1:
									prod.sku = str(matriz[i][j]).encode('utf-8')
								elif j == 2:
									prod.name = matriz[i][j].encode('utf-8')
								elif j == 3:
									prod.description = matriz[i][j].encode('utf-8')
								elif j == 4:										
									prod.color=matriz[i][j].encode('utf-8').split(",")
									color=matriz[i][j].encode('utf-8')
								#elif j == 5:
								#	try:
								#		price = str(int(matriz[i][j]))
								#	except:
								#		price = 0
								elif j == 5:
									price_sell = str(matriz[i][j])									
								elif j == 6:
									prod.manufacturer = matriz[i][j].encode('utf-8')	
								elif j == 8:
									cellar_name= matriz[i][j].encode('utf-8')
								elif j == 9:
									prod.brand = matriz[i][j].encode('utf-8')
								elif j == 11:
									try:
										q = k + j
										quantity=str(matriz[i][q])
										#recovering identified

										prod.InitWithSku(prod.sku)
										# product_id=prod.identifier
										operation="sell"

									#products stored for cellar
									
										cellar.InitWithName(cellar_name)
										cellar.RemoveProducts(prod.sku, quantity, price_sell, size, color, operation, self.get_user_email() )
									except:
										pass	
							# except:
							# 	dn="t3"
							# 	self.redirect("/product?dn="+dn)				
					
					#product is saved
					#prod.Save()	

					#recovering identified
					# prod.InitWithSku(prod.sku)
					# product_id=prod.identifier

					# #products stored for cellar
					# try:	
					# 	cellar.InitWithName(cellar_name)
					# 	cellar.RemoveProducts(prod.sku, quantity, price, size, color, operation) #mejorar salidas 
					# except:
					# 	pass
				# fnout=""		
				self.redirect("/product/out")
			else:
				dn="t2"
				self.redirect("/product/out?dn="+dn)
		else:
			dn="t2"
			self.redirect("/product/out?dn="+dn)
