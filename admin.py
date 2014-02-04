import webapp2
import jinja2
import os
import json
import logging
import datetime
import csv
from StringIO import StringIO
from urllib import quote, urlencode
from google.appengine.api import urlfetch

from models import Contributor

import headers

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
    	[os.path.join(os.path.dirname(__file__), "templates"),
    	os.path.join(os.path.dirname(__file__), "templates", "admin")]))

class AdminPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('admin/index.html')
		
		template_values = {}

		self.response.out.write(template.render(template_values))		


class AddContributor(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('admin/add-contributor.html')
		
		template_values = {'contributors' : Contributor().query().order(Contributor.profile_path)}

		self.response.out.write(template.render(template_values))

	def post(self):

		profile_path = self.request.get("profile_path")

		if not profile_path:
			abort(400)

		contributor = Contributor(id=profile_path, profile_path=profile_path)

		form_data = self.request.POST

		if "twitter_handle" in form_data:
			contributor.twitter_handle = form_data['twitter_handle']

		if "twitter_brand_handle" in form_data:
			contributor.twitter_brand_handle = form_data['twitter_brand_handle']
		
		contributor.put()

		self.redirect('/admin/add-contributor')

app = webapp2.WSGIApplication([
	('/admin', AdminPage),
	('/admin/add-contributor', AddContributor),],
                              debug=True)