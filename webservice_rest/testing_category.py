import sys
import urllib
import pymongo
from model10.basemodel import db

token = urllib.urlopen("http://localhost:8888/access_token?appid=100").read()

#######################
######## addig ########
#######################

category_name = "categoria"
add_data = urllib.urlopen("http://localhost:8888/category/add?token="+token+"&name=" + category_name).read()

print "addd {}".format(add_data)

cnt = db.category.find({"name":category_name}).count()

if cnt >= 1:
	print "testing ok"
else:
	print "testing failed"

print "\n\n"

#######################
######## list #########
#######################

list_category = urllib.urlopen("http://localhost:8888/category/list?token="+token+"&page=1&items=10").read()

print "list : {}".format(list_category)

print "\n\n"

#######################
######## find #########
#######################

print "http://localhost:8888/category/find?token="+token+"&name=" + category_name

find_category = urllib.urlopen("http://localhost:8888/category/find?token="+token+"&name=" + category_name).read()
print "find : {}".format(find_category)

print "\n\n"

#######################
######## remove #######
#######################

remove_data = urllib.urlopen("http://localhost:8888/category/remove?token="+token+"&name=" + category_name).read()

print "remove : {}".format(remove_data)

cnt = db.category.find({"name":category_name}).count()

if cnt == 0:
	print "test ok"
else:
	print "test failed"
