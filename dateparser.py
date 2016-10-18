#!/usr/bin/python

#import  os
#import  sys
#import  urllib2
import  re
import  datetime
from datetime import timedelta as td

class   table:
    def __init__(self):
        self.months =['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.thisyear = datetime.date.today().year
        self.lowdate = datetime.date(2001,1,1)
        self.highdate = datetime.date(2100,1,1)

        return
    
    def parseDates(self,datetext):
        x = re.findall(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2}',datetext)
        yr  =re.findall(',.*(201[4-9])',datetext)
        if not yr:
            yr  =['2016']
        if x:
            dateBeginMonth  =self.months.index(x[0].split()[0])
            dateBeginDay    =int(x[0].split()[1])
            dateEndMonth    =self.months.index(x[1].split()[0])
            dateEndDay      =int(x[1].split()[1])
            dateEndYear     =int(yr[0])

            if dateBeginMonth>dateEndMonth:
                dateBeginYear   =dateEndYear-1
            else:
                dateBeginYear   =dateEndYear

            if dateEndMonth==1 and dateEndDay==29:
                dateEndDay=28

            dateStart = datetime.date(dateBeginYear,dateBeginMonth+1,dateBeginDay)
            dateEnd = datetime.date(dateEndYear,dateEndMonth+1,dateEndDay)
        else:
            dateStart   =self.highdate
            dateEnd     =self.lowdate 

        return  {'start':dateStart, 'end':dateEnd}
    
    def parseElements(self,dates,rates):
        if rates:
            ratesTable = []
            i = 0
            mmdates = []
            ratenames = [rd.text for rd in rates[0]]
            for rw,rd in zip(rates[1:],dates[1:]):
                dates = self.parseDates(rd.text)
                zz = [dates['start'],dates['end']]
                mmdates.append(zz)
                ratesTable.append([zz,[self.parseRates(r.text) for r in rw]])

            mm = zip(*mmdates)
            maxdate = max(mm[1])
            mindate = datetime.date.today()
            for i,rt in enumerate(ratesTable):
                if rt[0][0] == self.highdate:
                    ratesTable[i][0][0] = mindate
                    ratesTable[i][0][1] = maxdate


            delta = maxdate - mindate
            self.calendar = []
            for i in range(delta.days+1):
                caldate  = mindate+td(days=i)
                rates = [[-1]*len(ratenames)]
                for rt in ratesTable:
                    if rt[0][0]<=caldate<=rt[0][1]:
                        rates.append(rt[1])
                if len(rates)>1:
                    rates = [max(x) for x in zip(*rates)]
                else:
                    rates = rates[0]
#TODO combine the following 2 lines
                rates = [float('nan') if r<0 else r for r in rates] 
                rates = dict(zip(ratenames,rates))
                self.calendar.append([caldate,rates])
        else:
            self.calendar = []
            
        return self.calendar

    def parseRates(self,rates):
        rates   =(rates.replace('$','').replace(',',''))
        if rates:
            rates = float(rates.split()[0])
        else:
            rates = -1.0
        return  rates

