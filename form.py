#Import statements
from google.appengine.ext import ndb

class Suggestion(ndb.Model):
    """ Suggestion class for passing to Google's cloud engine
    """
    #Properties to pass
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    subject = ndb.StringProperty()
    message = ndb.StringProperty()
