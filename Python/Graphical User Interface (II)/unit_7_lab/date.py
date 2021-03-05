
# Module to find the current date and time and format them as a string.

import datetime

def getDate():
    return datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")
