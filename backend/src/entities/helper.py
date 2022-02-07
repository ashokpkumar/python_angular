import hashlib
import datetime
from datetime import datetime,timedelta,date
import calendar
# convert string to list  
def stringToList(string):
    li = list(string.split(","))
    for i in li:
        if i=="":
            li.remove(i)#removed null value from list
    return li
    
#convert list to string
def listToString(list):
    string =''
    for i in list:
        if i=="":
            list.remove(i)
        else:
            string = i + "," + string
    string[:-1]
    return string

def hash_password(input_raw_password):
    sha_signature = hashlib.sha256(input_raw_password.encode()).hexdigest()
    return sha_signature
    
def date_validation(date):
    try:
        return datetime.datetime.strptime(date, "%d/%m/%Y").date()
    except:
        pass
    return ""

firstweekday = 6
def weeks_in_month(year, month):
        c = calendar.Calendar(firstweekday)
        for weekstart in filter(lambda d: d.weekday() == firstweekday, c.itermonthdates(year, month)):
            weekend = weekstart + timedelta(6)
            yield (weekstart, weekend)
            
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)