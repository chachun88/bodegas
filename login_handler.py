from basehandler import BaseHandler

class LoginHandler(BaseHandler):

	def get(self):
		self.clear_cookie("user")
		self.render("login.html", next=self.get_argument("next", "/"))

	def post(self):
		username = self.get_argument("user", "")
		password = self.get_argument("password", "")

		auth = False
		if username == "sodimac" and password == "sodimac123":
			auth = True

		if auth:
			self.set_current_user(username)
			self.redirect(self.get_argument("next", u"/"))
		else:
			error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
			self.redirect(u"/auth/login?e=" + error_msg)
