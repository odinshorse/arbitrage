
from time import gmtime, strftime

class plogger():

   logDir = ""

   def setLogDir(self,logDir):
       self.logDir = logDir

   def plogz(self,event):
       try:
           file = open(self.logDir, mode="a")
           time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
           file.write(time + " : " + event + "\n")
           file.close()
           return 1
       except:
           print("cannot log event: %s" % event)
           return 0 
