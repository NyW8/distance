# -*- coding: utf-8 -*-

class Country:
    """ Country class for information about countries including name, 
        languages, religions, ethnicities, customs, taboos, currency, 
        power, timezone, regulations, government type, and photos.
    """
    def __init__(self, name, lang, relig, eth, customs, taboos, curr_pow_time, regulations, government, photos = []):
        """ Initialization function, assigns all values to their corresponding input
        """
        self.name = name
        self.lang = lang
        self.relig = relig
        self.eth = eth
        self.customs = customs
        self.taboos = taboos
        self.curr_pow_time = curr_pow_time
        self.regulations = regulations
        self.government = government
        self.photos = photos
    def get_info(self):
        """ Returns all information about itself
        """
        return ({"name":self.name, "lang":self.lang, "relig":self.relig, "eth":self.eth, "customs":self.customs,
        "taboos":self.taboos,"curr_pow_time":self.curr_pow_time,"regulations":self.regulations,
        "government":self.government, "photos":self.photos})


#Initialize 6 countries for examples
israel = Country("Israel", ["Hebrew", "Arabic", "Russian"],
    ["Jewish", "Muslim", "Christian"], ["Jewish", "Arabic", "Other"],
    ["Very religious Jewish people of either gender do not acknowledge members of a different gender while greeting others.","Israelis are very open, so don\'t be afraid to talk about topics like politics-- but expect candor in return."],
    ["Israelis hate needless formality.", "nterethnic marriages, especially between Jewish and Arabic people, are frowned upon."], ["Shekel", "H type plug", ["GMT+3"]],
    ["Passport Validity: No minimum, but your stay cannot exceed validity of passport and airlines may deny boarding if your passport has less than 6 months validity.",
    "Blank Passport Pages: 1 page, normally aren\'t stamped upon entry", "Tourist Visa: Only if staying longer than 90 days", "Vaccinations: None",
    "Currency Restrictions: ENTRY/EXIT: If leaving or arriving by air you must declare amounts above 50,000 shekels and 12,00 shekels if by you came by land."],
    "Parliamentary democracy", ["../png/israel1.png", "../png/israel2.png", "../png/israel3.png", "../png/israel4.png", "../png/israel5.png", "../png/israel6.png"])

brazil = Country("Brazil", ["Portugese"],
    ["Roman Catholic", "No religion", "Assemblies of God", "Protestant"], ["White", "Multiracial", "Black"],
    ["Family is very important in Brazil, and kids will often live with their parents until their own marriage.", "If invited to a house, bring the host flowers or a small gift."],
    ["Avoid being more than 30 minutes late to dinner, and more than an hour late to a party.", "Do not raise religion in casual conversations."], ["Brazilian Real", "110/220/240 V", ["GMT-2", "GMT-4", "GMT-5"]],
    ["Tourist Visa: Yes", "Vaccinations: None", "Currency Restrictions: ENTRY/EXIT:  If more than 10,000 BR it must be declared."],
    "Constitutional Republic", ["../png/brazil1.png", "../png/brazil2.png", "../png/brazil3.png", "../png/brazil4.png", "../png/brazil5.png", "../png/brazil6.png"])

france = Country("France", ["French", "Arabic", "Portugese"],
    ["Christian","No religion", "Islam"], ["French", "French by Acquisition", "Immigrants", "Foreigners"],
    ['Meals are a very social process, and people take their time while eating together while chatting.'], ["The french language has honorifics, meaning that you speak to others differently depending on the formality and nature of the relationship. Keep in mind to use the right form of \'you\' in a conversation as to not disrespect who you\'re talking to.",
    'Never flaunt your wealth during a conversation.','Snapping your fingers is considered offensive.'],["Euro", "220/240 V", ["GMT+2"]],
    ["Passport Validity: Must be valid 3 months before departure", "Blank Passport Pages: at least one blank page", "Tourist Visa: Only if staying longer than 90 days.",
    "Vaccinations: None", "Currency Restrictions: ENTRY/EXIT: $10,000 euros"],
    "French Republic", ["../png/france1.png", "../png/france2.png", "../png/france3.png", "../png/france4.png", "../png/france5.png", "../png/france6.png"])

mexico = Country("Mexico", ["Spanish"],
    ["Roman Catholic", "Other Christian", "No religion"], ["White/European", "Indigenous", "Black"],
    ["At a small gathering, the host usually handles the introductions.", "It is polite to leave some food on your plate after a meal."], ['The okay sign is considered vulgar.','Men shouldnt put their hands in their pockets.','Putting your hands on your hips is considered making a challenge.','Religious profanity is very offensive.', "Do not sit down at dinner until you are invited and told where to sit."],
    ["Pesos", "127 V", ["PDT", "GMT-6"]],
    ["Passport Validity: Must be valid at entry", "Blank Passport Pages: 1 page per stamp", "Tourist Visa: Yes, if visiting more than 180 days",
    "Vaccinations: None", "Currency Restrictions:ENTRY/EXIT: $10,000"],
    "Federal Republic", ["../png/mexico1.JPEG", "../png/mexico2.JPEG", "../png/mexico3.JPEG", "../png/mexico4.JPEG", "../png/mexico5.JPEG", "../png/mexico6.JPEG"])

china = Country("China", ["Mandarin"],
    ["Chinese Folk Religion", "Buddhism", "Christianity"], ["Han Chinese", "Zhuang", "Hui"],
    ["Greetings are formal and the oldest person is usually greeted first."],
    ["Make sure to respect a Chinese person\'s personal space -- they value it very much!"], ["Yuan", "220 V", ["GMT+8"]],
    ["Passport Validity: 6 months", "Blank Passport Pages: 2 pages per stamp", "Tourist visa: Yes", "Vaccinations: None",
    "Currency Restrictions:ENTRY/EXIT: Max RMB 20,000"],
    "Communist Government", ["../png/china1.JPEG", "../png/china2.JPEG", "../png/china3.JPEG", "../png/china4.JPEG", "../png/china5.JPEG", "../png/china6.JPEG"])

southafrica = Country("South Africa", ["Zulu", "Xhosa", "Afrikaans", "English", "Northern Sotho"],
    ["Protestant", "No religion", "Catholic"], ["Black African", "Coloured", "White", "Indian/Asian"],
    ["Gifts in South Africa are opened when received.", "Be sure to arrive on time when invited to dinner."],
    ["It is impolite to point with your index finger."], ["Rand", "230v", ["GMT+2"]],
    ["Passport Validity: 30 days", "Blank Passport Pages: 2 consecutive empty pages per entry",
    "Tourist Visa: Required if visiting more than 90 days", "Vaccinations: Yellow Fever vaccine required at least 10 days before if travelling from certain countries",
    "Currency restrictions: ENTRY: ZAR 25,000; Foreign currency unlimited if declared; No Kruger coins. Exit: ZAR 25,000; Foreign currency unlimited if amount was declared on entry; Up to 15 Kruger coins if proof purchased with foreign currency"],
    "Parliamentary Democracy", ["../png/southafrica1.png", "../png/southafrica2.png", "../png/southafrica3.png", "../png/southafrica4.png", "../png/southafrica5.png", "../png/southafrica6.png"])


def return_country(name):
    """ Returns the country's information if it is available
    """
    if name == "Mexico":
        return mexico
    elif name == "France":
        return france
    elif name == "Israel":
        return israel
    elif name == "Brazil":
        return brazil
    elif name == "China":
        return china
    elif name == "South Africa":
        return southafrica
    else:
        return "Nope!"
