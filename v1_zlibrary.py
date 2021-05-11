#!/usr/bin/env python
#======================================================================================================================

import requests                                             # For downloading source code
import pandas as pd                                         # For displaying dataframe
from bs4 import BeautifulSoup as bs4                        # For extracting data from source code
from selenium import webdriver                              # For loading AJAX filled websites
import subprocess                                           # For opening the book in default app

#======================================================================================================================

import v1_languages as languages                                        # For searching language codes
import v1_rowInput as rowInput                                          # For asking and combing inputs
import v1_downloadCheck as downloadCheck                                # For checking if file has downloaded
import v1_renamer as renamer                                            # For renaming the file as per given param

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

def zlib(bookTitle, lang, ext, out):                        # (name, language, extension, output)

    initial_s = "https://b-ok.asia/s/"
    initial_b = "https://b-ok.asia"
    reqTitle  = bookTitle.replace(" ", "%20") + "/"

    #==========================================================

    if lang == None and ext == None:
        try:
            searchParam = requests.get(initial_s + reqTitle)
        except:
            print("Error in accessing Zlibrary.\n")
            return 404, 404

    elif ext == None:
        lang = lang.lower()
        try:
            searchParam = requests.get(initial_s + reqTitle, params = {"language":lang})
        except:
            print("Error in accessing Zlibrary.\n")
            return 404, 404

    elif lang == None:
        try:
            searchParam = requests.get(initial_s + reqTitle, params = {"extension":ext})
        except:
            print("Error in accessing Zlibrary.\n")
            return 404, 404

    else:
        lang = lang.lower()
        try:
            searchParam = requests.get(initial_s + reqTitle, params = {"language":lang, "extension":ext})
        except:
            print("Error in accessing Zlibrary.\n")
            return 404, 404

    #==========================================================
    
    if searchParam.status_code != 200:
        print("Error in accessing Zlibrary.\n")
        return 404, 404
    
    sourceCode = bs4(searchParam.content, "html5lib")
    results = sourceCode.find_all("div", {"class":"resItemBox resItemBoxBooks exactMatch"})

    for result in results:

        tempTitle = result.find("h3", {"itemprop":"name"}).find("a").get_text()
        tempLink = result.find("h3", {"itemprop":"name"}).find("a").get("href") 
        
        try:
            tempAuthor = result.find("a", {"itemprop":"author"}).get_text()
        except:
            # Author name might not exist
            tempAuthor = ""

        #==========================================================

        # Extracting language and extension for every book.
        detailBox = result.find_all("div",{"class":"property_value"})

        # Sample detail box includes {Year, Language, Extension}.
        if len(detailBox) != 3:
            for det in detailBox:
                comma = det.get_text().find(",")
                if comma != -1:
                    tempExtension = det.get_text()[:comma].lower()
                else:
                    try:
                        int(det.get_text())
                    except:
                        tempLanguage = det.get_text().capitalize()

        else:
            tempLanguage = detailBox[1].get_text().capitalize()
            tempExtension = detailBox[2].get_text()[:detailBox[2].get_text().find(",")].lower()

        # Appending exact matches to list.
        books.append(Book(tempTitle, tempLanguage, tempAuthor, tempExtension, tempLink))

        # Displaying list as data frame.
        dataFrame.append([books[-1].title, books[-1].auth, books[-1].lang, books[-1].ext])
        
        #==========================================================
        
    if len(books) == 0:
        print("No results found on ZLibrary.\n")
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

    # Error code is 999
    if rowSelect == 999:
        return 999, 999
    
    # Deep Search code is 404
    elif rowSelect == 404:
        return 404, 404
    
    #==========================================================

    # Accessing edition page of openLib:
    tempLink = initial_b + books[rowSelect-1].link

    #/////////////////////////////////////////////////////

    # This code is required if downloads are not occuring using Chrome and a new method for verifying downloads is required.

    # sizeTxt = bs4(requests.get(tempLink).content, "html5lib").find("a", {"class":"btn btn-primary dlButton addDownloadedBook"}).get_text()
    # sizeFull = sizeTxt[sizeTxt.index(", ") + 2 : sizeTxt.index(")")]
    # size = float(sizeFull[:sizeFull.index(" ")]) 

    # print(sizeTxt)
    # print(sizeFull)
    # print(size)

    #/////////////////////////////////////////////////////

    # Accessing AJAX loaded webstite using selenium.

    try:
        browser = webdriver.Chrome("chromedriver") #download chromedriver and add the path here
        browser.minimize_window()
        browser.get(tempLink)
    except:
        print("Error in accessing Zlibrary via Selenium.\n")
        return 404, 404

    # Clicking on the download button.
    try:
        browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/div/div/div/div[2]/div[2]/div[1]/div[1]/div/a").click()
    except:
        print("Error in accessing Zlibrary element via Selenium.\n")
        return 404, 404

    # Continuously monitors download folder and returns name of file after download completion.
    fileName = downloadCheck.main_C()

    #==========================================================

    if out != None:
        downloadLocation = out + "." + books[rowSelect-1].ext
    else:
        bookTitle = bookTitle.replace(" ","_")
        bookTitle = bookTitle.rstrip("_")
        downloadLocation = bookTitle + "." + books[rowSelect-1].ext

    #==========================================================

    # Renaming book as required.
    if renamer.rename_dnld(fileName, downloadLocation) == 0:
        print("Opening the book...\n")
        subprocess.run(['open', "/Users/tanishbafna/Downloads/" + downloadLocation], check = True)
        return 999, 999
    
    else:
        print("Opening the book...\n")
        subprocess.run(['open', "/Users/tanishbafna/Downloads/" + fileName], check = True)
        return 999, 999

#======================================================================================================================