import sys
import urllib
import pymongo
from model10.basemodel import db

token = urllib.urlopen("http://localhost:8888/access_token?appid=100").read()


################
#### adding ####
################

print "adding product"

product_name = "testing_product"
product_sku = "1"

add_data = urllib.urlopen("http://localhost:8888/product/add?token="+token+"&sku="+product_sku+"&name="+product_name+"&description=alguna&brand=giani&category=zapatos").read()

print "add : {}".format(add_data)

#if product_name == db.product.find({"sku":product_sku})[0]["name"]:
#	print "test ok"
#else:
#	print "test failed"

find_data = urllib.urlopen("http://localhost:8888/product/find?token="+token+"&sku=" + product_sku).read()

print "find : {}".format(find_data)

print "\n\n"

################
#### listing ###
################

list_data = urllib.urlopen("http://localhost:8888/product/list?token="+token+"&page=1&items=10").read()

print "list products"
print "list : {}".format(list_data)

print "\n\n"

################
#### remove ####
################

remove_data = urllib.urlopen("http://localhost:8888/product/remove?token=53459d259ec9a746d0291cbc&sku=" + product_sku).read()

print "remove product"
print "remove : {}".format(remove_data)

remove_query = db.product.find({"sku":product_sku})

if remove_query.count() == 0:
	print "test ok"
else:
	print "test failed"