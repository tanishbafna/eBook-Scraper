#!/usr/bin/env python
#======================================================================================================================

import requests                                             # For downloading source code
import pandas as pd                                         # For displaying dataframe
from bs4 import BeautifulSoup as bs4                        # For extracting data from source code

#======================================================================================================================

import v1_languages as languages                                           # For searching language codes
import v1_rowInput as rowInput                                             # For taking and combing input
import v1_extensions as extensions                                         # For finding .extension

#======================================================================================================================

books = []                                                  # Contains all filtered book objects.
dataFrame = []                                              # Contains arrays of book fields for pandas.

#======================================================================================================================

class Book:

    def __init__(self, Title, Author, EdLink):

        self.title = Title
        self.auth = Author
        self.link = EdLink

class Editions:

    def __init__(self, ext, link):

        self.extType = ext
        self.edLink = link
#======================================================================================================================

def openlib(bookTitle, lang, ext, out):                      #(name, language, extension, output)

    #==========================================================

    if lang != None:
        lang = languages.openlib_langCode(lang)

        try:
            searchParam = requests.get("https://openlibrary.org/search", params={"title": bookTitle, "mode": "ebooks", "has_fulltext": "true", "language": lang})
        except:
            print("Error in accessing OpenLib.")
            return 404, 404

    else:
        try:
            searchParam = requests.get("https://openlibrary.org/search", params={"title": bookTitle, "mode": "ebooks", "has_fulltext": "true"})
        except:
            print("Error in accessing OpenLib.")
            return 404, 404

    if searchParam.status_code != 200:
        print("Error in accessing OpenLib.")
        return 404, 404

    sourceCode = bs4(searchParam.content, "html5lib")
    results = sourceCode.find_all("span", {"class": "details"})
    
    #==========================================================

    for result in results:

        temp = result.find_all("a", {"class": "results"})

        try:
            books.append(Book(temp[0].get_text(), temp[1].get_text(), temp[0].get("href")))
        except:
            books.append(Book(temp[0].get_text(), "", temp[0].get("href")))

        # Adding to pandas array of arrays:
        dataFrame.append([books[-1].title, books[-1].auth])

    # #==========================================================
         
    if len(books) == 0:
        print("No results found on OpenLibrary.\n")
        return 404, 404

    #==========================================================#

    # Plotting table:
    df = pd.DataFrame(dataFrame, columns = ["Title", "Author"])    
    df.index += 1
    df_string = df.to_string(justify="justify", col_space=20, max_colwidth=50)

    print("")
    print(df_string)
    print("")
    
    #==========================================================#

    # Asking and combing row input:
    rowSelect = rowInput.getInput(len(books), "Y")
    
    # Exit code
    if rowSelect == 999:
        return 999, 999

    # Deep search code
    if rowSelect == 404:
        return 404, 404

    #==========================================================

    # Accessing edition page of openLib:
    tempLink = "https://openlibrary.org/" + books[rowSelect-1].link

    try:
        result = requests.get(tempLink)
    except:
        print("Error in accessing OpenLib.")
        return 404, 404

    if result.status_code != 200:
        print("Error in obtaining mirror link. Try again.")
        return 404, 404

    soup = bs4(result.content, "html5lib")

    # Finding GET link:
    try:
        findLink = soup.find("ul",{"class":"ebook-download-options"}).find_all("a")
    except:
        print("No results found.")
        return 404, 404

    #==========================================================

    extensionsList = []
    
    # Internet archive recognizes txt format as plain text.
    if ext == "txt":
        ext = "plain text"

    for i in range(len(findLink)):

        # DAISY is an unreadable format.
        if findLink[i].get_text() == "DAISY":
            continue
        
        if ext == None:
            # Finding and printing all available extensions.
            extensionsList.append(Editions(extensions.extCode[findLink[i].get_text().lower()], findLink[i].get("href")))
            print(f"{i+1}.  {findLink[i].get_text()}")
        
        elif ext == findLink[i].get_text().lower():
            # Adding only that extension which matches param.
            extensionsList.append(Editions(extensions.extCode[findLink[i].get_text().lower()], findLink[i].get("href")))
            break

    #==========================================================

    print("")

    # Total available formats stored in extensionsList.
    rowSelect_EXT = len(extensionsList)

    # If more than one format available, let user choose. Else, start download.
    if rowSelect_EXT != 1:
        rowSelect_EXT = rowInput.getInput(rowSelect_EXT)

        # Exit code.
        if rowSelect_EXT == 999:
            return 999, 999

    # Obtaining link and type from user input. 
    link = extensionsList[rowSelect_EXT - 1].edLink
    ext = extensionsList[rowSelect_EXT - 1].extType

    #==========================================================

    if out != None:
        downloadLocation = "/" + out + ext
    else:
        bookTitle = bookTitle.replace(" ","_")
        bookTitle = bookTitle.rstrip("_")
        downloadLocation = "/" + bookTitle + ext
    
    #==========================================================

    return link, downloadLocation

#======================================================================================================================