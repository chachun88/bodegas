import sys
import urllib
import pymongo
from model10.basemodel import db


#######################
######## addig ########
#######################

print "adding"

token = urllib.urlopen("http://localhost:8888/access_token?appid=100").read()

user_email = "a@a.com"
user_name = "test"
user_pass = "test"

add_data = urllib.urlopen("http://localhost:8888/salesman/add?token="+token+"&name="+user_name+"&password="+user_pass+"&email=" + user_email).read()

print "add : {}".format(add_data)

add_query = db.salesman.find({"email":user_email})

if add_query.count() >= 1:
	print "testing ok"
else:
	print "testing failed"

print "\n\n"

#######################
######## listing ######
#######################

lis_data = urllib.urlopen("http://localhost:8888/salesman/list?token="+token+"&page=1&items=10").read()
print "list : {}".format(lis_data)

print "\n\n"

#######################
######## find #########
#######################

find_data = urllib.urlopen("http://localhost:8888/salesman/find?token="+token+"&email=" + user_email).read()

print "find : {}".format(find_data)

print "\n\n"

#######################
######## Remove #######
#######################

remove_data = urllib.urlopen("http://localhost:8888/salesman/remove?token="+token+"&email="+ user_email).read()

print "remove : {}".format(remove_data)

remove_query = db.salesman.find({"email":user_email}).count()

if remove_query == 0:
	print "testing ok"
else:
	print "testing failed"

print "\n\n"
