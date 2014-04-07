import sys
import urllib
import pymongo

from model.cellar import Cellar

### conection

connection  = pymongo.Connection("localhost", 27017)
db     = connection.market_tab

###functions
def getArgument(arg_name, default):
	is_next = False
	rtn_argument = default

	for arg in sys.argv:

		if is_next:
			rtn_argument = arg

		is_next = False
		if arg == arg_name:
			is_next = True

	return rtn_argument

## variable initialization
module = getArgument("-m", "")
test =  getArgument("-t", "")

ws_url = "http://localhost:8888/"

## getting access_token
token_url = urllib.urlopen(ws_url + "access_token?appid=100")
token = token_url.read()

print "\naccess token : " + token


def addTesting(add_data):
	print "\nrunning /cellar/add testing"
	add_url = ws_url + "cellar/add?" + urllib.urlencode(add_data)
	add_results = urllib.urlopen(add_url).read()

	cellar = Cellar()
	cellar.InitWithId(add_results, db.cellar)

	#print "results : " + cellar.name
	if cellar.name == add_data["name"]:
		print "ok"
	else:
		print "failed"
	print "testing results: " + add_results


	return add_results

def listTesting(list_data):

	#testing /cellar/list
	print "\nrunning /cellar/list testing"

	list_url = ws_url + "cellar/list?" + urllib.urlencode(list_data)
	list_results = urllib.urlopen(list_url).read()

	print "testing results : " + list_results

def editTesting(add_results, edit_data):
	print "\nrunning /cellar/edit testing"

	edit_data["id"] = add_results

	print "edit id: " + edit_data["id"]

	edit_url = ws_url + "cellar/edit?" + urllib.urlencode(edit_data)
	edit_results = urllib.urlopen(edit_url).read()

	cellar = Cellar()
	cellar.InitWithId(edit_results, db.cellar)

	print "cellar id: " + str(cellar.identifier)

	#print "testing results : " + cellar.name
	if cellar.name == edit_data["name"] and cellar.identifier == edit_data["id"]:
		print "ok"
	else:
		print "failed"

	return edit_results

def findTesting(edit_results, find_data):
	print "\nrunning /cellar/find testing"

	find_data["id"] = add_results

	find_url = ws_url + "cellar/find?" + urllib.urlencode(find_data)
	find_results = urllib.urlopen(find_url).read()
	print "testing results : "  + find_results

def removeTesting(edit_results, remove_data):
	print "\nrunning /cellar/remove testing"

	remove_data["id"] = edit_results

	remove_url = ws_url + "cellar/remove?" + urllib.urlencode(remove_data)
	remove_results = urllib.urlopen(remove_url).read()

	### search if removed
	data = ws_url + "cellar/find?" + urllib.urlencode(remove_data)
	data_results = urllib.urlopen(data).read()

	print "testing results : " + remove_results

def productsAddTesting(add_results, products_add_data):
	# products sample 1231233asidoad:10,qoiewiqoej1:1
	print "this testing must be builded"



if module == "cellar":

	##data
	add_data 	= {"name":"testing_cellar", "description": "this is a testing cellar", "token":token}
	list_data 	= {"page":1,"itmes":1, "token":token}
	edit_data 	= {"name":"testing_changed","description":"description changed","id":"", "token":token}
	find_data 	= {"id": "", "token":token}
	remove_data = {"id":"", "token":token}
	products_add_data = {"id":"", "token" : token, "products":""}

	if test == "":
		add_results = addTesting(add_data)
		edit_results = editTesting(add_results, edit_data)
		listTesting(list_data)
		findTesting(edit_results, find_data)
		removeTesting(edit_results, remove_data)

	elif test == "add":
		addTesting(add_data)

	elif test == "products":
		add_results = addTesting(add_data)
		productsAddTesting(add_results, products_add_data)

