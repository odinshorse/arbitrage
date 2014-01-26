#!/usr/bin/python

#########################################################################
#                       Re-usable bot library                           #
#                                by                                     #
#                            colonel panik                              #
#########################################################################


################################imports###################################

import re 
import httplib2 
import httplib 
import urllib 
import socks 
import time 
import random
import sys 
import os
import mechanize 
import cookielib
import plogger

from BeautifulSoup import BeautifulSoup
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

##################################bot_class#########################

class Bot():

##########################class_variables############################

    username = ""
    password = ""
    logfile = "./LOG/plog.log"
    startURL = ""
    loginURI = ""
    loginFormName = "login"
    spiderDir = ""

######################init############################################

    def __init__(self):

        #setup logger
        self.logger = plogger.plogger()
        self.logger.setLogDir(self.logfile)

        #setup browser
        self.browser = mechanize.Browser()
        self.cookieJar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookieJar)
        self.browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.04 (lucid) Firefox/3.6.18")]
        self.browser.set_handle_robots(False)

##########################set_username###############################

    def setUsername(self,username):
        self.username = username

############################set_password#############################
 
    def setPassword(self,password):
        self.password = password

#############################return_username########################

    def getUsername(self):
        return self.username

#######################return_password################################

    def getPassword(self):
        return self.password

#####################set_logfile########################################

    def setLogfile(self,logfile):
        self.logfile = logfile

####################set_starting_point##################################
        
    def setStartURL(self,startURL):
        self.startURL = startURL

######################set_login_page_URL##########################

    def setLoginURI(self,URI):
        self.loginURI = URI

#####################set_login_form_name##########################

    def setLoginFormName(self,name):
        self.loginFormName = name

######################set_directory_to_crawl######################

    def setSpiredDir(self,spiderDir):
        self.spiderDir = spiderDir

#######################add_log_entry################################

    def log(self,event):
        self.logger.plogz(event)

##########################are_we_logged_out?########################

    def isLoggedOut(self,content,regex):
        match = regex.search(str(content))
        if (match):
            return True
        else:
            return False

#######################do_cookie_based_login#########################

    def login(self,queryString,regex):
        #request start page and login
        response = self.browser.open(self.startURL)
        self.randumbSleep()
        #debug print response.read()

        self.browser.select_form(name=self.loginFormName)

        for name,value in queryString.items():
            self.browser[name] = value
        

        response = self.browser.submit()
        #debug print response.read()
        if(not self.isLoggedOut(response.read(),regex)):
            return True
        else:
            return False

#######################do_post_request###############################

    def post(self,URL,QueryString,headers=None):
        
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cookieJar))
        if headers:
            opener.addheaders = headers
        qs = urllib.urlencode(QueryString)
        response = opener.open(URL,qs)
        return response

########################do_get_request###############################

    def get(self,URL,QueryString=None,headers=None):

        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(self.cookieJar))
        if headers:
            opener.addheaders = headers
        content = "" 

        if (QueryString):
            qs = urllib.urlencode(QueryString)
            response = opener.open(URL + '?' + qs)
            content = response

        else:
            response = opener.open(URL)
            content = response

        return content

########################upload_multipart_files########################

    def multipartPost(self,URL,content):
        return "test"

########################find_nonce_tokens##############################

    def findNonceFields(self,content):

        try:

            soup = BeautifulSoup(str(content))
            fields = soup.findAll('input',{'type':'hidden'})
            regex = re.compile(r'(?<=\<input\stype\=\"hidden\"\sname\=\")(?P<name>.*?)(\"\svalue\=\")(?P<value>.*?)(\")')
            regex2 = re.compile(r'(?<=\<input\stype\=\"hidden\"\svalue\=\")(?P<value>.*?)(\"\sname\=\")(?P<name>.*?)(\"\>)')
            names = []
            values = [] 

            for field in fields:

                matches = regex.finditer(str(field))
                matches2 = regex2.finditer(str(field))

                for match in matches:

                    names.append(match.group('name'))
                    values.append(match.group('value'))

                for match2 in matches2:

                    names.append(match2.group('name'))
                    values.append(match2.group('value'))
   
            return names,values

        except:

            return 0,0

##########################add_entropy_to_be_more_human####################

    def randumbSleep(self):
        time.sleep(random.randint(10, 21))

########################random_sleep_for_file_uploads#####################

    def randumbSleepForFiles(self):
        time.sleep(random.randint(60, 121))
