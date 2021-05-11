#!/usr/bin/env python
#======================================================================================================================

import os
from time import sleep

#======================================================================================================================

file = ".crdownload"
    
def checker():

    global file

    ls = os.listdir("/")

    # Checks every item in download folder and attatches z-lib file's name to variable.
    for item in ls:
        if item.find("z-lib") != -1:
            file = item
            break

#======================================================================================================================

def main_C():

    global file 

    # Loop continues as long as download is not completed.
    while file.find(".crdownload") != -1:
        sleep(3)
        checker()
    
    # Returns name of downloaded file.
    return file

#======================================================================================================================