import sys
import urllib
import pymongo
from model10.basemodel import db

token = urllib.urlopen("http://localhost:8888/access_token?appid=100").read()

#######################
######## addig ########
#######################

brand_name = "marca"
add_data = urllib.urlopen("http://localhost:8888/brand/add?token="+token+"&name=" + brand_name).read()

print "addd {}".format(add_data)

cnt = db.brand.find({"name":brand_name}).count()

if cnt >= 1:
	print "testing ok"
else:
	print "testing failed"

print "\n\n"

#######################
######## list ########
#######################

list_brand = urllib.urlopen("http://localhost:8888/brand/list?token="+token+"&page=1&items=10").read()

print "list : {}".format(list_brand)

print "\n\n"

#######################
######## find #########
#######################

find_brand = urllib.urlopen("http://localhost:8888/brand/find?token="+token+"&name=" + brand_name).read()
print "find : {}".format(find_brand)

print "\n\n"

#######################
######## remove #######
#######################

remove_data = urllib.urlopen("http://localhost:8888/brand/remove?token="+token+"&name=marca").read()

print "remove : {}".format(remove_data)

cnt = db.brand.find({"name":brand_name}).count()

if cnt == 0:
	print "test ok"
else:
	print "test failed"
