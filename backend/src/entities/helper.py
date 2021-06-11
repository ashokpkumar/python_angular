# convert string to list  
def helper1(string):
    li = list(string.split(","))
    return li
#convert list to string
def helper2(list):
    string =''
    for i in list:
        string =i + "," + string
    string[:-1]
    return string
#remove null values in list
def removenull(list):
    for i in list:
            if i=="":
                list.remove(i)