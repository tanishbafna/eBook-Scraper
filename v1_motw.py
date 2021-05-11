#!/usr/bin/env python
#======================================================================================================================

import requests                                             # For downloading source code
import pandas as pd                                         # For displaying dataframe
import json                                                 # For turning a strings to dictionaries

#======================================================================================================================

import v1_rowInput as rowInput                                             # For taking and combing input

#======================================================================================================================

books = []                                                  # Contains all filtered book objects.
dataFrame = []                                              # Contains arrays of book fields for pandas.

#======================================================================================================================

class Book:

    def __init__(self, Title, Author, Extension, Link):

        self.title = Title
        self.auth = Author
        self.ext = Extension
        self.link = Link   

#======================================================================================================================

def MemoryOfTheWorld(bookTitle, ext, out):                      #(name, language, extension, output)

    #==========================================================

    searchUrl = bookTitle.replace(" ", "%20")
    try:
        searchParam = requests.get("https://books.memoryoftheworld.org/search/titles/" + searchUrl)
    except:
        print("Error in accessing Memory of the World.\n")
        return 404, 404

    if searchParam.status_code != 200:
        print("Error in accessing Memory of the World.\n")
        return 404, 404

    # Loading string to a json.
    temp = json.loads(searchParam.content)
    results = temp["_items"]

    #==========================================================

    for result in results:
        
        #==========================================================

        tempExt = []

        # Index number of required extension.
        formatIndex = 303

        for form in range(len(result["formats"])):

            if ext != None:
            
                if result["formats"][form]["format"].lower() == ext.lower():
                    tempExt = [result["formats"][form]["format"].lower()]
                    formatIndex = form
                    break
            
            else:
                tempExt.append(result["formats"][form]["format"].lower())

        # If required extension not found, next iteration. 
        if ext != None and formatIndex == 303:
            continue
        
        # If no param then choosing only first element in formats dict.
        if ext == None:
            formatIndex = 0

        #==========================================================
        
        # If only one extension available or asked for:
        if len(tempExt) == 1:
            tempLink = ["https:" + result["library_url"] + result["formats"][formatIndex]["dir_path"] + result["formats"][formatIndex]["file_name"]]
        
        # If multiple formats available:
        else:
            tempLink = []
            for form in result["formats"]:
                tempLink.append("https:" + result["library_url"] + form["dir_path"] + form["file_name"])

        #==========================================================
        
        # Formatting authors with a comma seperator.
        if len(result["authors"]) == 1:
            tempAuth = result["authors"][0]
        
        else:
            tempAuth = ""
            for a in result["authors"]:
                tempAuth += a + ", "
            
            tempAuth = tempAuth.rstrip(", ")

        #==========================================================

        books.append(Book(result["title"], tempAuth, tempExt, tempLink))

        #==========================================================
        
        # Printing extensions with a pipe seperator.
        if len(tempExt) == 1:
            tempExt = tempExt[0]

        else:
            temptempExt = ""
            for e in tempExt:
                temptempExt = temptempExt + e + " | "
            
            tempExt = temptempExt.rstrip(" | ")

        #==========================================================

        dataFrame.append([books[-1].title, books[-1].auth, tempExt])

    #==========================================================
         
    if len(books) == 0:
        print("No results found on MOTW.\n")
        return 404, 404

    #==========================================================

    # Plotting table:
    df = pd.DataFrame(dataFrame, columns = ["Title", "Author", "Extension"])    
    df.index += 1
    df_string = df.to_string(justify="justify", col_space=20, max_colwidth=50)

    print("")
    print(df_string)
    print("")
    
    #==========================================================

    # Asking and combing row input:
    rowSelect = rowInput.getInput(len(books), "Y")

    # Exit code
    if rowSelect == 999:
        return 999, 999
    
    # Deep search code
    elif rowSelect == 404:
        return 404, 404
    
    #==========================================================

    # If many versions available:
    if len(books[rowSelect-1].ext) > 1:

        # Serial No.
        i = 0

        for e in books[rowSelect-1].ext:
            print(f"{i+1}.  {e.capitalize()}")
            i += 1

        print("")
        selectIndex = rowInput.getInput(len(books[rowSelect-1].ext)) - 1

        # Exit code.
        if selectIndex == 999:
            return 999, 999

    # If only one version available (first element):
    else:
        selectIndex = 0
    #==========================================================

    if out != None:
        downloadLocation = "/" + out + "." + books[rowSelect-1].ext[selectIndex]
    else:
        bookTitle = bookTitle.replace(" ","_")
        bookTitle = bookTitle.rstrip("_")
        downloadLocation = "/" + bookTitle + "." + books[rowSelect-1].ext[selectIndex]
    
    #==========================================================

    # Choosing link of selected version.
    link = books[rowSelect - 1].link[selectIndex]

    return link, downloadLocation

#======================================================================================================================