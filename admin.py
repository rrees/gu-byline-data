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
from google.appengine.ext import ndb

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
			webapp2.abort(400, "A profile path is required")

		if not profile_path.startswith("/profile/"):
			webapp2.abort(400, "Profile path should be /profile/<byline-slug-name>")

		contributor = Contributor(id=profile_path, profile_path=profile_path)

		form_data = self.request.POST

		if "twitter_handle" in form_data:
			contributor.twitter_handle = form_data['twitter_handle']

		if "twitter_brand_handle" in form_data:
			contributor.twitter_brand_handle = form_data['twitter_brand_handle']
		
		contributor.put()

		self.redirect('/admin/add-contributor')

class RemoveContributor(webapp2.RequestHandler):
	def post(self):
		profile_path = self.request.get("profile_path")

		if not profile_path:
			webapp2.abort(400, "A profile path is required")

		contributor = ndb.Key('Contributor', profile_path).get()

		if not contributor:
			webapp2.abort(404, "Contributor with profile path {profile_path} not found".format(profile_path=profile_path))

		#logging.info(contributor)

		contributor.key.delete()

		self.redirect('/admin/add-contributor')

class EditContributor(webapp2.RequestHandler):
	def get(self, contributor_key):
		template = jinja_environment.get_template('admin/edit-contributor.html')

		key = ndb.Key(urlsafe=contributor_key)
		
		template_values = {'contributor' : key.get()}

		self.response.out.write(template.render(template_values))

	def post(self, contributor_key):

		#logging.info(self.request.POST)

		key = ndb.Key(urlsafe=contributor_key)

		contributor = key.get()

		if contributor:

			field_names = ['profile_path', 'twitter_handle', 'twitter_brand_handle', 'google_plus_id']
			required_fields = ['profile_path', 'twitter_handle']

			for field in field_names:
				if field in self.request.POST:
					value = self.request.POST[field].strip()
					if len(value) < 1 and field in required_fields:
						continue
					setattr(contributor, field, value if len(value) > 0 else None)

			contributor.put()


		self.redirect('/admin/edit-contributor/' + contributor_key)

app = webapp2.WSGIApplication([
	('/admin', AdminPage),
	('/admin/add-contributor', AddContributor),
	('/admin/remove-contributor', RemoveContributor),
	webapp2.Route(r'/admin/edit-contributor/<contributor_key>', handler=EditContributor)],
                              debug=True)