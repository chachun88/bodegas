import pymongo

from bson import json_util
from basemodel import BaseModel, db
from salesman import Salesman
from cellar import Cellar
from product import Product
from kardex import Kardex

####################################
########## basemodel.py ############
####################################

print "testing basemodel.py"

base_model = BaseModel()
base_model.identifier = ""

## remove empty
print "error : {}".format(base_model.Remove())

## adding item
print "adding: "
base_model.identifier = db.base_testing.save({"_id":"un_id"})
val_1 = db.base_testing.find().count()
message = base_model.Remove()
val_2 = db.base_testing.find().count()


status = "fail"

if val_1 == 1 and val_2 == 0:
	status = "ok"

print message
print "1: {} -- 2: {} -- status: {}".format(val_1, val_2, status)

print "\n\n"

####################################
########## salesman.py #############
####################################

sales_man = Salesman()

print "salesman testing"
print "error : "
print sales_man.InitByEmail("fake@bad.com")

sales_man.name = "test"
sales_man.password = "test"
sales_man.email = "fake@bad.com"
sales_man.identifier = "1"

## save and load
print "save: {}".format(sales_man.Save())
print "cnt : {}".format(db.salesman.find().count())
print "load: {}".format(sales_man.InitByEmail("fake@bad.com"))

## login
print "login: {}".format(sales_man.Login("fake@bad.com", "test"))

## permissions
print "permissions : {}".format(sales_man.AssignPermission("admin"))
print "permissions : {}".format(sales_man.AssignPermission("user"))
print "permissions : {}".format(sales_man.GetPermissions())

## delete
print "remove : {}".format(sales_man.RemovePermission("user"))
print "permissions : {}".format(sales_man.GetPermissions())
print "user_remove : {}".format(sales_man.Remove())
print "user init : {}".format(sales_man.InitByEmail("fake@bad.com"))

print "\n\n"

####################################
########### cellar.py ##############
####################################

cellar = Cellar()

cellar.name = "primera bodega"
cellar.description = "esta es la primera bodega"
cellar.identifier = "534db54f9ec9a77e7440f03c"

print "cellar testing"
print "save : {}".format(cellar.Save())
print "rename : {}".format(cellar.Rename("otro nombre"))
print "list : {}".format(json_util.dumps(Cellar.GetAllCellars()))
#print "remove : {}".format(cellar.Remove())

print "\n\n"

####################################
########### product.py #############
####################################

product = Product()

product.name = "nuevo producto"
product.description = "a product description"
product.sku = "123"
product.brand = "a brand"
product.color = "red"
product.size = "10"
product.image = "an image"
product.manufacturer = "giani"

print "product.py"
print "print : {}".format(product.Print())
print "save: {}".format(product.Save())
print "print : {}".format(product.Print())
print "init : {}".format(product.InitBySku("123"))
print "list : {}".format(product.GetList(0,10))
#print "remove : {}".format(product.Remove())

print "\n\n"

####################################
########### kardex.py ##############
####################################

kardex = Kardex()

kardex.product_identifier = product.identifier
kardex.cellar_identifier = cellar.identifier
kardex.date = 20140416

##clean kardex
db.kardex.remove({
	"product_identifier":kardex.product_identifier,
	"cellar_identifier":kardex.cellar_identifier
	})

kardex.operation_type = Kardex.OPERATION_BUY
kardex.units = 40
kardex.price = 50000

print "Insert : {}".format(kardex.Insert())

kardex.operation_type = Kardex.OPERATION_SELL
kardex.units = 4

kardex.Insert()

kardex.operation_type = Kardex.OPERATION_SELL
kardex.units = 30

kardex.Insert()

kardex.operation_type = Kardex.OPERATION_BUY
kardex.units = 15
kardex.price = 50000

kardex.Insert()

kardex.operation_type = Kardex.OPERATION_BUY
kardex.units = 60
kardex.price = 52000

kardex.Insert()


kardex.operation_type = Kardex.OPERATION_SELL
kardex.units = 65.0

kardex.Insert()


kardex.Debug(product.identifier, cellar.identifier)


















