#!/usr/bin/env python
#======================================================================================================================

import os

#======================================================================================================================

def rename_dnld(fileName, downloadLocation):

    # Store cwd to return to it.
    cwd = os.getcwd()

    # Go to dir and rename.
    os.chdir("/")
    try:
        os.rename(fileName, downloadLocation)
        os.chdir(cwd)
        return 0

    except:
        print("Error Renaming.")
        os.chdir(cwd)
        return -1

#======================================================================================================================