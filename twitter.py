import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import headers

from models import Contributor

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

twitter_data = [('Paul Harris', 'paulxharris'),
	('Karen McVeigh', 'karenmcveigh1'),
	('Ed Pilkington', 'edpilkington'),
	('Adam Gabbatt', 'AdamGabbatt'),
	('Matt Wells', 'MatthewWells'),
	('Hadley Freeman', 'HadleyFreeman'),
	('Richard Adams', 'RichardA'),
	('Suzanne Goldenberg', 'suzyji'),
	('Chris McGreal', 'chrismcgreal'),
	('Dominic Rushe', 'dominicru'),
	('Stuart Millar', 'stuartmillar159'),
	('Brian Braiker', 'slarkpope'),
	('Laurence Topham', 'loztopham'),
	('Matt Williams', 'mattywills'),
	('Ruth Spencer', 'onthewag'),
	('Ryan	Devereaux', 'Rdevro'),
	('Tom McCarthy', 'TeeMcSee'),
	('Ewen MacAskill', 'ewenmacaskill'),
	('Amanda Michel', 'amichel'),
	('Steve Busfield', 'Busfield'),
	('Katie Rogers', 'katierogers'),
	('Owen Gibson', 'owen_g'),
	('Danny Taylor', 'DTGuardian'),
	('Dominic Fifield', 'domfifield'),
	('Donald McRae', 'donaldgmcrae'),
	('Barney Ronay', 'barneyronay'),
	('David Hytner', 'DaveHytner'),
	('Stuart James', 'StuartJamesGNM'),
	('Sid Lowe', 'sidlowe'),
	('Raphael Honigstein', 'honistein'),
	('Marcus Christenson', 'm_christenson'),
	('James Dart', 'James_Dart'),
	('Barry Glendenning', 'bglendenning'),
	('Sachin Nakrani', 'SachinNakrani'),
	('Jacob Steinberg', 'JacobSteinberg'),
	('Paul Wilson', 'paulwilsongnm'),
	('Jamie Jackson', 'GuardianJamieJ'),
	('Paul Doyle', 'Paul_Doyle'),
	('Matt Seaton', 'mattseaton'),
	('Jonathan Freedland', 'Freedland'),
	('David Hills', 'd_hills'),
	('Juliette Garside', 'JulietteGarside'),
	]
contributors = [{"name" : name, "twitter_handle" : handle} for (name, handle) in twitter_data]

cache_seconds = 60 * 60

class AllBylines(webapp2.RequestHandler):
	def get(self):

		headers.json(self.response)
		headers.set_cors_headers(self.response)
		headers.set_cache_headers(self.response, cache_seconds)
		self.response.out.write(json.dumps(contributors))

twitter_lookup = {
	"Owen Gibson" : {
		"personal" : "owen_g",
		"brand" : "guardianfootball"
	},
	"Jonathan Freedland" : {
		"personal" : "Freedland"
	},
	"David Hills" : {
		"personal" : "d_hills",
		"brand" : "guardianfootball"
	}
}

brand_by_country = {
	"AU" : "GuardianAus",
	"US" : "GuardianUS"
}

class BylineLookup(webapp2.RequestHandler):
	def post(self):

		byline = self.request.get("byline", None)
		country = self.request.headers["X-AppEngine-Country"]

		if not byline:
			abort(400)

		headers.json(self.response)
		headers.set_cors_headers(self.response)
		headers.set_cache_headers(self.response, cache_seconds)

		data = twitter_lookup[byline]

		if not "brand" in data:
			data["brand"] = brand_by_country.get(country, "guardian")

		self.response.out.write(json.dumps(data))

class ProfilePathLookup(webapp2.RequestHandler):
	def get(self):

		profile_path = self.request.get("profile_path", None)
		country = self.request.headers["X-AppEngine-Country"]

		if not profile_path:
			abort(400)

		headers.json(self.response)
		headers.set_cors_headers(self.response)
		headers.set_cache_headers(self.response, cache_seconds)

		key = ndb.Key(Contributor, profile_path)
		contributor = key.get()

		if not contributor:
			abort(404)

		data = {
			"personal" : contributor.twitter_handle,
			"brand" : brand_by_country.get(country, "guardian")
		}

		if contributor.twitter_brand_handle:
			data['brand'] = contributor.twitter_brand_handle

		self.response.out.write(json.dumps(data))
app = webapp2.WSGIApplication([
	('/api/twitter/all', AllBylines),
	('/api/twitter/lookup/byline', BylineLookup),
	('/api/twitter/lookup', ProfilePathLookup),
	],
                              debug=True)
