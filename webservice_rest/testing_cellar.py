import sys
import urllib
import pymongo
from model10.basemodel import db

token = urllib.urlopen("http://localhost:8888/access_token?appid=100").read()


################
#### adding ####
################
print "adding cellar"

cellar_name = "testing_cellar"
cellar_id = ""

print "http://localhost:8888/cellar/add?token="+token+"&name="+cellar_name+"&description=this+is+a+testing+cellar"
add_cellar = urllib.urlopen("http://localhost:8888/cellar/add?token="+token+"&name="+cellar_name+"&description=this+is+a+testing+cellar").read()
print add_cellar

data = db.cellar.find({"name":cellar_name})

cellar_id = str(data[0]["_id"])

if data[0]["name"] == cellar_name:
	print "testing ok"
else:
	print "testing failed"

print "\n\n"

################
#### finding ###
################

cellar_data = urllib.urlopen("http://localhost:8888/cellar/find?token="+token+"&id=1").read()

print "finding"
print "error : {}".format(cellar_data)
cellar_data = urllib.urlopen("http://localhost:8888/cellar/find?token="+token+"&id=" + cellar_id).read()
print "ok    : {}".format(cellar_data)

print "\n\n"

################
#### listing ###
################

print "cellar listing"
cellar_list = urllib.urlopen("http://localhost:8888/cellar/list?token="+token+"&page=1&items=10").read()
print cellar_list

print "\n\n"

################
#### remove ####
################

print "cellar remove"
remove = urllib.urlopen("http://localhost:8888/cellar/remove?token="+token+"&id="+cellar_id).read()
print remove

cnt = db.cellar.find({"name":cellar_name}).count()

if cnt == 0:
	print "testing ok"
else:
	print "testing failed"
