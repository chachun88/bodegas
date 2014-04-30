#!/usr/bin/python
# -*- coding: UTF-8 -*-

## transform a number to money format
def MoneyFormat(number):

	# str_number = "$ "

	# counter = 0
	# for x in str(number):
	# 	if counter % 3 == 0 and counter != 0:
	# 		str_number += "."
	# 	#str_number += x
	# 	counter += 1

	# return "{}".format(str_number)

	import math
	return '$' + str(format(math.floor(number * 100) / 100, ',.0f'))
