#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from threading import Timer

class lpEmailTool(object):

	PLAIN_TEXT = 1
	HTML_CONTENT = 2

	WS_FUNCTION = "mailling"
	#WS_URL = "http://localhost:9004/"
	WS_URL = "http://mailling.loadingplay.com/"

	"""docstring for lpEmailTool"""
	def __init__(self):

		self._ffrom = ""
		self._password = ""
		self._tto = ""
		self._subject = ""
		self._content =  ""
		self._content_type = lpEmailTool.PLAIN_TEXT
		pass

	@property
	def ffrom(self):
	    return self._ffrom
	@ffrom.setter
	def ffrom(self, value):
	    self._ffrom = value
	
	@property
	def password(self):
	    return self._password
	@password.setter
	def password(self, value):
	    self._password = value
	
	@property
	def tto(self):
	    return self._tto
	@tto.setter
	def tto(self, value):
	    self._tto = value
	
	@property
	def subject(self):
	    return self._subject
	@subject.setter
	def subject(self, value):
	    self._subject = value
	
	@property
	def content(self):
	    return self._content
	@content.setter
	def content(self, value):
	    self._content = value
	
	@property
	def content_type(self):
	    return self._content_type
	@content_type.setter
	def content_type(self, value):
	    self._content_type = value

	def SendEmail(self):

		def send():
			data_params = {'from':self.ffrom, 
							'to':self.tto,
							'password':self.password,
							'subject':self.subject,
							'content':self.content,
							'content_type':self.content_type
							}

			params = urllib.urlencode(data_params)
			rtn_data = urllib.urlopen(self.WS_URL + self.WS_FUNCTION, params)

			print str(rtn_data.read())

		timer = Timer(0.1, send)
		timer.start()