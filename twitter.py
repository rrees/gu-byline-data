import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class AllBylines(webapp2.RequestHandler):
	def get(self):
		data = {}

		headers.json(self.response)
		headers.set_cors_headers(self.response)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/api/twitter/all', AllBylines)],
                              debug=True)