
#Import statements
import webapp2
import json
from google.appengine.api import urlfetch
import logging
import jinja2
from country import *
from form import Suggestion

#Creating variables for template loading
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader= template_loader)

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
    def get(self):
        #Get template and country's name
        template = template_env.get_template('html/country.html')
        country_name = self.request.get("country_name")
        test = return_country(country_name)
        
        #Log info for debugging
        logging.info(str(test)+" "+str(type(test)))
        
        #Render that country's template
        self.response.write(template.render(test.get_info()))

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

        #Try to access the internet to get the currencies
        try:
            result = urlfetch.fetch(url)

            #Check that site could be reached
            if result.status_code == 200:

                #Change result.content from string to dictuionary
                listDictionary = json.loads(result.content)

                #Returns dictionary of currency ids and names
                currencies = {}
                count = 0
                countList = []
                
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
            
        #Catch url not found errors
        except urlfetch.Error:
            logging.exception("Unable to get values: url is invalid")

            
    def getConversion(self):
        """ Helper function to get a certain conversion rate
        """
        #API url
        url = "http://www.apilayer.net/api/live?access_key=26d090d35324a4b7dd821d34068f354d"

        try:
            #If internet is available, load the conversion rates
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                listDictionary = json.loads(result.content)["quotes"]
                return listDictionary
        except urlfetch.Error:
            loggin.exception("Unable to find conversion rates: url is invalid")

            
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
        all_currencies = self.getNames("0")

        #Get names of chosen currencies
        from1 = self.getNames(int(curr1))
        to1 = self.getNames(int(curr2))

        #Get both conversion factors
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
    ('/country_details', Countries),    #Country details page
    ('/currency', Currency),            #Currency converter page
    ('/suggestions', Suggestions),      #Suggestions form page
    ('/thankyou', ThankYou),            #Thank you page (for after submitting a suggestion
    ('/packing', Packing),              #Packing list page
    ('/misc', Misc),                    #Miscellaneous travel info page
    ('/about.*', About),                #About us page
    ('/sources', Sources),              #Sources page
    ('/.*', MapPage),                   #Main map page/handles every call not to another page
], debug = True)
