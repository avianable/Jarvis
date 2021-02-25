
''' Dictionary to hold name and email ids '''

emailDict = {
    "name" : "emailId@gmail.com"
     
}

''' Returns the name from email-id'''

def getName(emailId) : 
    dict_val = list(emailDict.values())
    dict_keys = list(emailDict.keys())

    name = dict_keys[dict_val.index(emailId)]
    name = name.capitalize()
    return name

# name = getName("anukritikajal@gmail.com")
# print(name)