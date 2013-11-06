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

authors = [
		{
			name: 'Paul Harris',
			twitter_handle: 'paulxharris'
		},

		{
			name: 'Karen McVeigh',
			twitter_handle: 'karenmcveigh1'
		},

		{
			name: 'Ed Pilkington',
			twitter_handle: 'edpilkington'
		},

		{
			name: 'Adam Gabbatt',
			twitter_handle: 'AdamGabbatt'
		},

		{
			name: 'Matt Wells',
			twitter_handle: 'MatthewWells'
		},

		{
			name: 'Hadley Freeman',
			twitter_handle: 'HadleyFreeman'
		},

		{
			name: 'Richard Adams',
			twitter_handle: 'RichardA'
		},

		{
			name: 'Suzanne Goldenberg',
			twitter_handle: 'suzyji'
		},

		{
			name: 'Chris McGreal',
			twitter_handle: 'chrismcgreal'
		},

		{
			name: 'Dominic Rushe',
			twitter_handle: 'dominicru'
		},

		{
			name: 'Stuart Millar',
			twitter_handle: 'stuartmillar159'
		},

		{
			name: 'Brian Braiker',
			twitter_handle: 'slarkpope'
		},

		{
			name: 'Laurence Topham',
			twitter_handle: 'loztopham'
		},

		{
			name: 'Matt Williams',
			twitter_handle: 'mattywills'
		},

		{
			name: 'Ruth Spencer',
			twitter_handle: 'onthewag'
		},

		{
			name: 'Ryan Devereaux',
			twitter_handle: 'Rdevro'
		},

		{
			name: 'Tom McCarthy',
			twitter_handle: 'TeeMcSee'
		},

		{
			name: 'Ewen MacAskill',
			twitter_handle: 'ewenmacaskill'
		},

		{
			name: 'Amanda Michel',
			twitter_handle: 'amichel'
		},

		{
			name: 'Steve Busfield',
			twitter_handle: 'Busfield'
		},

		{
			name: 'Katie Rogers',
			twitter_handle: 'katierogers'
		},
        {
            name: 'Owen Gibson',
            twitter_handle: 'owen_g'
        },
        {
            name: 'Danny Taylor',
            twitter_handle: 'DTGuardian'
        },
        {
            name: 'Dominic Fifield',
            twitter_handle: 'domfifield'
        },
        {
            name: 'Donald McRae',
            twitter_handle: 'donaldgmcrae'
        },
        {
            name: 'Barney Ronay',
            twitter_handle: 'barneyronay'
        },
        {
            name: 'David Hytner',
            twitter_handle: 'DaveHytner'
        },
        {
            name: 'Stuart James',
            twitter_handle: 'StuartJamesGNM'
        },
        {
            name: 'Sid Lowe',
            twitter_handle: 'sidlowe'
        },
        {
            name: 'Raphael Honigstein',
            twitter_handle: 'honistein'
        },
        {
            name: 'Marcus Christenson',
            twitter_handle: 'm_christenson'
        },
        {
            name: 'James Dart',
            twitter_handle: 'James_Dart'
        },
        {
            name: 'Barry Glendenning',
            twitter_handle: 'bglendenning'
        },
        {
            name: 'Sachin Nakrani',
            twitter_handle: 'SachinNakrani'
        },
        {
            name: 'Jacob Steinberg',
            twitter_handle: 'JacobSteinberg'
        },
        {
            name: 'Paul Wilson',
            twitter_handle: 'paulwilsongnm'
        },
        {
            name: 'Jamie Jackson',
            twitter_handle: 'GuardianJamieJ'
        },
        {
            name: 'Paul Doyle',
            twitter_handle: 'Paul_Doyle'
        },
        {
			name: 'Matt Seaton',
			twitter_handle: 'mattseaton'
		}
	]

class AllBylines(webapp2.RequestHandler):
	def get(self):
		data = {}

		headers.json(self.response)
		headers.set_cors_headers(self.response)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/api/twitter/all', AllBylines)],
                              debug=True)
