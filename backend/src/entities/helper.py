import hashlib
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