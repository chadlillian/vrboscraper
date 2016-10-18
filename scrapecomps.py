#!/home/chad/anaconda/bin/python

from pymongo import MongoClient
import propertyStats as props

import time

DATABASE = 'VRBO'
DATABASE = 'VRBO_scenic_hwy_98'
PROPERTIES = 'Properties'
STATS = 'Stats'
CALENDAR = 'Calendars'
link = 'https://www.vrbo.com/'

class driverstuff():
    def __init__(self,database):
        self.unit = props.propertyStats()

        self.client = MongoClient()
        self.db = self.client[database]
        self.stats = self.db['Stats']
        self.calendars = self.db['Calendar']
        self.collection = self.db['Properties']

####    REMOVE:::
#        self.calendars.remove()
#        self.stats.remove()

        self.properties = self.collection.find()

    def findAllProperties(self,daysold):
        olderthan = time.time()-daysold*24*60*60
        notupdated = {'updated':{'$exists':False}}
        old = {'updated':{'$lt':olderthan}}
        query = {"$or":[notupdated,old]}
        self.properties = [x['_id'] for x in self.collection.find(query)]
        #print len(self.properties)
      
    def readAllProperties(self):
        for prop in self.properties:
            self.readSingleProperty(link,prop)
            self.collection.update_one({'_id':prop},{'$set':{'updated':time.time()}})
        
    def readSingleProperty(self,link,num):
        start = time.time()
        try:
            stats = self.unit.readProperty(link+str(num))
            stats['_id'] = num
            self.stats.save(stats)

            aa = self.calendars.find({'_id':num})
            #for ai in aa[0]:
            #  print ai,aa[0][ai]
            stats = self.unit.readCalendar()
            stats['_id'] = num
            self.calendars.save(stats)
        except:
            None
        #print num,time.time()-start

    def showAllProperties(self):
        properties = self.collection.find()
        #for prop in properties:
        #    print prop

if __name__=="__main__":
    a = driverstuff(DATABASE)
    a.findAllProperties(0.0)
    a.readAllProperties()
    #a.showAllProperties()
