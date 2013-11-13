from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class Contributor(ndb.Model):
	profile_path = ndb.StringProperty(required=True)
	twitter_handle = ndb.StringProperty()
	twitter_brand_handle = ndb.StringProperty()
	google_plus_id = ndb.StringProperty()