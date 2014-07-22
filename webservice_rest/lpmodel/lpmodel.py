#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import os

f = open ('genmymodel.uml', 'r')
file_data = f.read().replace("uml:", "uml_").replace("xmi:", "xmi_") ## translate uml to common xml
file_data = file_data.strip()

root = ET.fromstring(file_data)

## find class name
def findClassName(identifier):
	for cls in root.findall('packagedElement'):
		if identifier == cls.get('xmi_id'):
			return cls.get('name')

	return ""


## getting all packagedElement
for cls in root.findall('packagedElement'):

	## class variables
	parent_class = "object"
	class_name = cls.get('name')
	attributes = []
	operations = []

	## getting parent class
	try:
		general_id = cls.find('generalization')
		
		if hasattr(general_id, "get"):
			parent_class = findClassName(general_id.get('general'))
	except Exception, e:
		raise

	## looping attributes
	for attr in cls.findall('ownedAttribute'):
		attributes.append({"name":attr.get("name"), "type":"String"}) # TODO : fix this value

	## lopping operations
	for op in cls.findall('ownedOperation'):

		operation = {"name":op.get("name"), "is_static":False, "return":"String", "parameters":[]} # TODO : fix this value

		#if hasattr(op, "isStatic"):
		operation["is_static"] = bool(op.get("isStatic"))

		## looping parameters
		for param in op.findall("ownedParameter"):
			if param.get("name") != "returnParameter":
				operation["parameters"].append({"name":param.get("name")})

		operations.append(operation)

	##debugging
	# print "\n\n"
	# print class_name
	# print parent_class
	# print attributes
	# print operations

	## generate_class string

	## config
	class_string = "#!/usr/bin/python\n"
	class_string += "# -*- coding: UTF-8 -*-\n"
	##imports
	class_string += "\n"
	if parent_class != "object":
		class_string += "from " + parent_class.lower() + " import " + parent_class + "\n"
		class_string += "\n"

	## class init 
	class_string += "class " + class_name + "(" + parent_class + "):\n"
	class_string += "	def __init__(self):\n"
	class_string += "		"+parent_class+".__init__(self)\n"

	## init attributes all are strigs for now
	for attr in attributes:
		class_string += "		self._" + attr["name"] + " = ''\n"

	## adding attributes with getter and setter
	for attr in attributes:
		class_string += "\n" 
		class_string += "	@property\n"
		class_string += "	def " + attr["name"] + "(self):\n"
		class_string += "		return self._" + attr["name"] + "\n"
		class_string += "	@" + attr["name"] + ".setter\n"
		class_string += "	def " + attr["name"] + "(self, value):\n"
		class_string += "		self._" + attr["name"] + " = value\n"

	## adding operations to class
	for op in operations:
		
		class_string += "\n"
		if op["is_static"]:
			class_string += "	@staticmethod\n"
			class_string += "	def " + op["name"] + "("
		else:
			class_string += "	def " + op["name"] + "(self"

		# adding parameters
		first_iteration = True
		for param in op["parameters"]:
			if op["is_static"] and first_iteration:
				class_string += param["name"]
			else:
				class_string += ", " + param["name"]

		class_string += "):\n"
		class_string += "		return ''\n"

	## writing class
	print class_string
	file_name = "model/" + class_name.lower() + ".py"
	ddir = os.path.dirname(file_name)

	try:
		os.stat(ddir)
	except Exception, e:
		os.mkdir(ddir)

	ffile = open(file_name, "w")

	try:
		ffile.write(class_string)
	finally:
		ffile.close()

	# ffile = open("model/" + class_name + ".py", "w")
	# ffile.append(class_string)