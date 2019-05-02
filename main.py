
#Import statements
import webapp2
import json
from google.appengine.api import urlfetch
import logging
import jinja2
from country import *
from form import Suggestion

from bs4 import BeautifulSoup
import requests


#Creating variables for template loading
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader= template_loader)

def get_json(url):
	try:
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			return (json.loads(result.content))
	except urlfetch.Error:
		logging.exception("Unable to get info from "+str(url))

def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match

class MapPage(webapp2.RequestHandler):
	""" Handles the main page (Map page), and renders it
	"""
	def get(self):
		#Find and render the template
		template=template_env.get_template('html/map.html')
		self.response.write(template.render())

class Countries(webapp2.RequestHandler):
	""" Handles calls to different countries for more info on them
	"""
	def getPhotos(self, country_name):
		#Get pageid for the photos
		url = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=Tourism_in_"+country_name
		result = get_json(url)
		pageid = result["query"]["search"][0]["pageid"]
		logging.info("pageid: "+ str(pageid))

		#Get photos themselves
		url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid="+str(pageid)
		result = get_json(url)
		html_from_result = result["parse"]["text"]["*"]
		photos = []
		#Add all the photos to the array
		soupJ = BeautifulSoup(html_from_result, 'html.parser')
		for img in soupJ.findAll('img', alt=True):
			if (img['alt'] == "" and not("flag" in img.get('src').lower() or "logo" in img.get('src').lower() or "icon" in img.get('src').lower() ) ):
				photos.append(img.get('src'))

		return(photos)

	def getPage(self, country_name):
		url = "https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+country_name
		listDictionary = get_json(url)
		#Change result.content from string to dictionary
		#listDictionary = json.loads(result.content)
		
		pageid = listDictionary["query"]["search"][0]["pageid"]
		logging.info("pageid: "+ str( pageid))
		
		url = "https://en.wikipedia.org/w/api.php?action=parse&format=json&pageid="+str(pageid)
		result = get_json(url)
		name = result["parse"]["title"]
		photos = self.getPhotos(name)

		soup = BeautifulSoup(result["parse"]["text"]["*"], "html.parser")
		infobox = soup.find_all(match_class(["infobox", "geography", "vcard"]))[0]

		all_data = {}
		for row in infobox.find_all("tr"):
			info = row.find_all("th")
			data = row.find_all("td")
			if (len(info) != 0 and len(data) != 0):
				key = info[0].text.encode("utf-8").strip()
				value = data[0].text.encode("utf-8").strip()
				if (key in all_data):
					all_data[key].append(value)
				else:
					all_data[key] = [value]
				

		logging.info("SOUP ENDS HERE")
		languages = []			#list of languages most used (or maybe just national languages?)
		religions = []
		currency = all_data["Currency"][0]
		government = all_data["Government"][0]			#type of government
		#TODO: get all data below from the html page:
		for language in all_data["National language"]:
			languages.append(language)
		for religion in all_data["Religion"]:
			religions.append(religion)

		#TODO: get data for these:
		ethnicities = []
		timezones = []
		customs = []
		taboos = []
		regulations = []		#travel regulations
		power = ""				#power type
		
		logging.info(all_data)
		new_country = Country(name, languages,  religions, ethnicities,
			customs, taboos, [currency, power, timezones], regulations, government, photos)
		
		return (new_country)
	
	def get(self):
		#Get template and country's name
		template = template_env.get_template('html/country.html')
		country_name = self.request.get("country_name")
		#test = return_country(country_name)
		country = self.getPage(country_name)
		#logging.info("COUNTRY REQUESTED: "+str(country.get_info()["name"]))
		
		#Render that country's template
		self.response.write(template.render(country.get_info()))

class Currency(webapp2.RequestHandler):
	""" Currency convertion page, uses currency api from apilayer
		and converts number to another currency
	"""
	
	def getNames(self, search):
		""" Helper function for currency class, uses an API to return a 
			list of currencies and their current values relative to the US Dollar
		"""
		#Our api url
		url = 'http://apilayer.net/api/list?access_key=26d090d35324a4b7dd821d34068f354d'
		listDictionary = get_json(url)

		#Returns dictionary of currency ids and names
		currencies = {}
		count = 0
		#countList = []
		
		#Returns a sorted dictionary of values and indexes
		for value in sorted(listDictionary["currencies"].values()):
			currencies[count] = value
			count+=1
		if search == "0":
			return currencies
		else:
			val = currencies[search]
			val2 = [key for (key, value) in listDictionary["currencies"].items() if value == val][0]
		#Return values
		return val2

			
	def getConversion(self):
		""" Helper function to get a certain conversion rate
		"""
		#API url
		url = "http://www.apilayer.net/api/live?access_key=26d090d35324a4b7dd821d34068f354d"
		listDictionary = get_json(url)
		return listDictionary
			
	def get(self):
		""" Original currency page, shows the currency template
			with the names of each available currency
		"""
		#Find and render the template, set the current currency to the first alphabetically
		template = template_env.get_template('html/currency.html')
		self.response.write(template.render({"currencies":self.getNames("0")}))

		
	def post(self):
		""" Converts chosen currency amount to second currency
		"""
		#Get initial data from user
		curr1 = int(self.request.get("curr1"))
		curr2 = int(self.request.get("curr2"))
		amount1 = self.request.get("amount1")
		#all_currencies = self.getNames("0")

		#Get names of chosen currencies
		from1 = self.getNames(int(curr1))
		to1 = self.getNames(int(curr2))

		#Get both conversion factors
		convert_currencies1 = 1
		convert_currencies2 = 1
		if (from1 != to1):
			convert_currencies1 = self.getConversion()["USD"+to1]
			convert_currencies2 = self.getConversion()["USD"+from1]
		
		amount2 = 0
		
		#Check that amount is valid
		if amount1 == "" or amount1 < 0:
			amount1 = 0
		else:
			conversion = float(convert_currencies1)/float(convert_currencies2)
			amount2 = float(amount1)*conversion
		template = template_env.get_template('html/currency.html')
		
		#Log info
		logging.info("CURRENCY INFO REQUEST from: "+from1+ " amt: "+str(amount1)+" to: "+to1+" amt: "+str(amount2))
		#Send data to template
		self.response.write(template.render({"currencies":self.getNames("0"), "curr1":curr1, "curr2":curr2,"amt1":amount1, "amt2":amount2}))

class Suggestions(webapp2.RequestHandler):
	""" Handles calls to the suggestions page of the website
	"""
	def get(self):
		#Find and render template
		template = template_env.get_template('html/suggestionstest.html')
		self.response.write(template.render())
		
class ThankYou(webapp2.RequestHandler):
	""" Thank you page for after submitting a suggestion
	"""
	def post(self):
		template = template_env.get_template('html/thankyou.html')
		
		#Get message and provided info
		sugg_name = self.request.get("name-input")
		subj = self.request.get("subject-field")
		email = self.request.get("email-input")
		message = self.request.get("message")
		
		#Send info to server
		suggest = Suggestion(name=sugg_name, email=email, subject = subj, message=message)
		suggest.put()
		dictdict = {"sugg_name":sugg_name}
		
		#Pass back name for personalization
		self.response.write(template.render(dictdict))
		
class Misc(webapp2.RequestHandler):
	""" Handles calls to the miscellaneous travel tips page
	"""
	def get(self):
		#Find and render template
		template = template_env.get_template('html/misc.html')
		self.response.write(template.render())

class About(webapp2.RequestHandler):
	""" Handles calls to the About Us page
	"""
	def get(self):
		#Find and render template
		template = template_env.get_template('html/about.html')
		self.response.write(template.render())
		
class Packing(webapp2.RequestHandler):
	""" Handles calls to the packing list page
	"""
	def get(self):
		#Find and render template
		template = template_env.get_template('html/packinglist.html')
		self.response.write(template.render())

class Sources(webapp2.RequestHandler):
	""" Handles calls to the sources page
	"""
	def get(self):
		#Find and render template
		template = template_env.get_template('html/sources.html')
		self.response.write(template.render())
		
#Send calls to the correct class, thereby rendering the correct template
app = webapp2.WSGIApplication([
	('/country_details', Countries),	#Country details page
	('/currency', Currency),			#Currency converter page
	('/suggestions', Suggestions),	  #Suggestions form page
	('/thankyou', ThankYou),			#Thank you page (for after submitting a suggestion
	('/packing', Packing),			  #Packing list page
	('/misc', Misc),					#Miscellaneous travel info page
	('/about.*', About),				#About us page
	('/sources', Sources),			  #Sources page
	('/.*', MapPage),				   #Main map page/handles every call not to another page
], debug = True)

