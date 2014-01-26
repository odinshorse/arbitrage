#!/usr/bin/python

########################################################################
#                                                                      #
#                          Bitcoin Arbitrage System                    #
#                                    by:                               #
#                                Jolly Roger                           #
#                                                                      #
########################################################################



################################imports#################################

import bot
import re
import plogger
import mechanize
import cookielib
import json as simplejson
import hmac
import urllib
import hashlib
import time


#############################Vircurex-Class###################################

class vircurex(bot.Bot):

    name = "Vircurex"
    price = None
    currentBalance = None
    transactionFee = None

####################LoginInfo#######################

    username = ""
    password = ""
    secret = ""
    tid = ""

####################################################

    #setup
    def __init__(self):

        #setup logger
        self.logger = plogger.plogger()
        self.logger.setLogDir(self.logfile)

        #setup browser
        self.browser = mechanize.Browser()
        self.cookieJar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookieJar)
        self.headers = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.04 (lucid) Firefox/3.6.18")]
        self.browser.addheaders = self.headers
        #self.headersV2 = {"User-agent":"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.04 (lucid) Firefox/3.6.18"}
        self.browser.set_handle_robots(False)

######################################################

    def makeToken(self, token_string, params):
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S", tuple(time.gmtime()))
        params = tuple([self.secret, self.username, stamp, self.tid] + list(params))

        token = hashlib.sha256(token_string % params).hexdigest()
        return stamp, token

########################################################

    def apiCall(self):

        stamp,token = makeToken(self.username)



######################################################

    #set self.price from vircurex exchange.
    def setPrice(self):
        resp = self.get("https://vircurex.com/api/get_last_trade.json?base=LTC&alt=BTC", headers = self.headers)
        data = simplejson.load(resp)
        self.price = float(data["value"])
        return self.price

##################################################

    #get self.price
    def getPrice(self):
        return self.price


###############################BTCe-Class############################################

class BTCe(bot.Bot):

    name = "BTCe"
    price = None
    currentBalance = None
    transactionFee = float(.002)

    #API info
    apiKey = "1TIDHALV-4EJOAIXW-6QRUF33Y-BANPVI5L-2I35FFTY"
    apiSecret = "d495dcb3f2ea4dded1bd6c2109c8e41b870e0674bb4f25e4b3eee9fa8946f56b"

    nonce = None

###################################################

    #setup
    def __init__(self):

        #setup nonce
        self.nonce = str(time.time()).split('.')[0]

        #setup logger
        self.logger = plogger.plogger()
        self.logger.setLogDir(self.logfile)

        #setup browser
        self.browser = mechanize.Browser()
        self.cookieJar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookieJar)
        self.headers = [("User-agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0")]
        self.browser.addheaders = self.headers
        #self.headersV2 = {"User-agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0"}
        self.browser.set_handle_robots(False)

#####################################################


    #get request for api calls
    def apiCall(self,URL,headers=None,params=None):

        params2 = None
        if params:
            params2 = urllib.urlencode(params)

        #sign headers
        signed = self.apiSign(params2)
        #add headers
        apiHeaders = [("Content-type", "application/x-www-form-urlencoded"),("Key", self.apiKey,),("Sign", signed)]

        if headers:
            headers = headers + apiHeaders
        else:
            headers = apiHeaders
        #do post request
        resp = self.post(URL,params,headers=headers)
        #reset nonce for next request to trading api
        self.nonce = str(time.time()).split('.')[0]
        return resp

########################################################

    #api signing algorythm
    def apiSign(self,params):
        return hmac.new(self.apiSecret,params,digestmod=hashlib.sha512).hexdigest()


########################################################

    #set self.price from btc-e ticker api
    def setPrice(self):

        resp = self.get("https://btc-e.com/api/2/ltc_btc/ticker")
        data = simplejson.load(resp)
        self.price = float(data["ticker"]["buy"])
        return self.price

#######################################################


    #get price from self.price
    def getPrice(self):
        return self.price

########################################################

    #get and organize current account info
    def getInfo():
        resp = self.apiCall("https://btc-e.com/tapi/", headers=self.headers, params={"method":"getInfo","nonce": str(self.nonce)})







###################################################################################
#                                                                                 #
#                             Arbitrage Utilities                                 #
#                                                                                 #
###################################################################################

class Arbitrage():

    exchange1 = BTCe()
    exchange2 = vircurex()
    exchanges = [exchange1,exchange2]

    highExchange = None #name of high exchange
    lowExchange = None #name of low exchange

    #def __init__(self): #nothing initialized yet

##################sorting_related_algorithms#####################3

################################################

    #find closest of 2 values to a third value.
    def closestValue(self,value1,value2,target):

        v1 = 0
        v2 = 0

        v1 = abs(value1 - target)
        v2 = abs(value2 - target)

        if v1 > v2:
            #print value2
            return value2
        else:
            #print value1
            return value1

################################################

    #ascending quick sort for exchanges by price
    def sortByHighPrice(self,exchanges):

        if exchanges == []:
            return []

        else:

            pivot = exchanges[0]

            lesser = self.sortByHighPrice([exchange for exchange in exchanges[1:] if exchange.price < pivot.price])
            greater = self.sortByHighPrice([exchange for exchange in exchanges[1:] if exchange.price > pivot.price])

            return lesser + [pivot] + greater

#################################################

    #get the high exchange in BTC
    def getHighBTC(self):
        return highExchange.price

################################################

    #get the low exchange in BTC
    def getLowBTC(self):
        return lowExchange.price

################################################

    #get the price of exchange1
    def getExchange1Price(self):
        return self.exchange1.getPrice()

##################################################

    #get the price of exchange2
    def getExchange2Price(self):
        return self.exchange2.getPrice()

#################################################

    #download current trading price from exchange1
    def setExchange1Price(self):
        return self.exchange1.setPrice()

###################################################

    #download current trading price from exchange2
    def setExchange2Price(self):
        return self.exchange2.setPrice()

###################################################

    #set exchanges (for after they have been sorted)
    def setExchanges(self,exchangesArray):
        self.exchanges = exchangesArray




#############################Test-Code###############################

arb = Arbitrage()
arb.setExchange1Price()
arb.setExchange2Price()

arb.setExchanges(arb.sortByHighPrice(arb.exchanges))

print str(arb.exchanges[0].price) + " : " + str(arb.exchanges[0].name) + " = The Low Exchange"
print str(arb.exchanges[len(arb.exchanges) - 1].price) + " : " + str(arb.exchanges[len(arb.exchanges) - 1].name) + " = The High Exchange"
