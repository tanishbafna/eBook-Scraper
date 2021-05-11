#!/usr/bin/env python
#========================================================== Import Libraries

import requests                                             # For downloading source code
import pandas as pd                                         # For displaying dataframe
from bs4 import BeautifulSoup as bs4                        # For extracting data from source code

#======================================================================================================================

import v1_languages as languages                                           # For searching language codes
import v1_rowInput as rowInput                                             # For taking and combing input

#======================================================================================================================

books = []                                                  # Contains all filtered book objects.
dataFrame = []                                              # Contains arrays of book fields for pandas.

#======================================================================================================================

class Book:

    def __init__(self, Title, Language, Author, Extension, Link):

        self.title = Title
        self.lang = Language
        self.auth = Author
        self.ext = Extension
        self.link = Link   

#======================================================================================================================

def libgen(bookTitle, lang, ext, out):                      #(name, language, extension, output)

    #==========================================================

    try:
        searchParam = requests.get("http://gen.lib.rus.ec/search.php", params={"req": bookTitle, "res": 100, "sort": "title", "sortmode": "ASC"})
    except:
        print("Error in accessing Libgen.\n")
        return 404, 404

    if searchParam.status_code != 200:
        print("Error in accessing Libgen.\n")
        return 404, 404

    sourceCode = bs4(searchParam.content, "html5lib")
    results = sourceCode.find("table", {"class": "c"}).find_all("tr")[1:]
    
    #==========================================================

    for result in results:

        temp = result.find_all("td")
        links = temp[9].find("a").get("href")
        
        #Filters:
        if lang != None and ext != None:

            if temp[6].get_text().find(lang) == -1:
                continue
            if temp[8].get_text() != ext:
                continue
        
        elif lang != None:

            if temp[6].get_text().find(lang) == -1:
                continue
        
        elif ext != None:

            if temp[8].get_text() != ext:
                continue
        
        # Creating book object:
        books.append(Book(Title=temp[2].get_text(), Language=temp[6].get_text(), Author=temp[1].get_text(), Extension=temp[8].get_text(), Link=links))

        # Adding to pandas array of arrays:
        dataFrame.append([books[-1].title, books[-1].auth, books[-1].lang, books[-1].ext])

    #==========================================================
         
    if len(books) == 0:
        print("\nNo results found on Libgen.\n")
        return 404, 404

    #==========================================================

    # Plotting table:
    df = pd.DataFrame(dataFrame, columns = ["Title", "Author", "Language", "Extension"])    
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

    if out != None:
        downloadLocation = "/" + out + "." + books[rowSelect-1].ext
    else:
        bookTitle = bookTitle.replace(" ","_")
        bookTitle = bookTitle.rstrip("_")
        downloadLocation = "/" + bookTitle + "." + books[rowSelect-1].ext
    
    #==========================================================
    
    # Calling download function:
    return download(books[rowSelect-1].link, downloadLocation)

#======================================================================================================================

def download(link, downloadLocation):

    #==========================================================

    try:
        result = requests.get(link)
    except:
        print("Error in accessing Libgen.\n")
        return 404, 404

    if result.status_code != 200:
        print("Error in obtaining Libgen mirror link.")
        return 404, 404

    soup = bs4(result.content, "html5lib")

    # Finding GET link:
    findLink = soup.find("table").find("tr").find_all("td")[1].find("h2").find("a").get("href")
    
    #==========================================================

    return findLink, downloadLocation

#======================================================================================================================
#======================================================================================================================