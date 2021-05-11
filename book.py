#!/usr/bin/env python
#======================================================================================================================

from sys import argv                                        # For obtaining command line arguments
import getopt                                               # For parsing command line arguments

#======================================================================================================================

import v1_languages as languages                                          # Find languages and codes
import v1_dnldFin as dnldFin                                              # For downloading book

#======================================================================================================================

def main(bookTitle, lang, ext, out):

    import v1_libgen as libgen
    link, downloadLocation = libgen.libgen(bookTitle, lang, ext, out)
    
    # Deeper search code: 404
    # Exit code: 999
    
    if link == 404:
        import v1_archive as archive
        link, downloadLocation = archive.openlib(bookTitle, lang, ext, out)

        if link == 404:
            import v1_zlibrary as zlibrary
            link, downloadLocation = zlibrary.zlib(bookTitle, lang, ext, out)

            if link == 404:
                import v1_motw as motw
                link, downloadLocation = motw.MemoryOfTheWorld(bookTitle, ext, out)

                if link == 404:
                    quit()

    if link == 999:
        quit()

    return dnldFin.BookDownloader(link, downloadLocation)

#======================================================================================================================

def commandLine():

    global argv

    # Initial value of Libgen Params set to None:
    title = None
    lang = None
    ext = None
    out = None

    # Transforming argv[] to a string seperated by single space:
    commandLine_Arg = ""
    for i in range(1, len(argv)):
        commandLine_Arg += argv[i] + " "

    # Seperating title and other optional arguments:
    if commandLine_Arg.find(" -") != -1:
        title = commandLine_Arg[:commandLine_Arg.find(" -")]
        if title == "" or title == " ":
            title = None

    else:
        title = commandLine_Arg
        if title == "" or title == " ":
            title = None


    if title == None:
        print("No book title entered [enter title after 'book.py']")
        quit()

    #==========================================================


    # Turning string back to list for extracting arguments: 
    argumentList = commandLine_Arg[commandLine_Arg.find(" -"):].split()
    options = "l:x:o:"
    long_options = ["Language=", "Extension=", "Output="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        if False:
            print(values)

        for currentArgument, currentValue in arguments: 
            
            if currentArgument in ("-l", "--Language"): 
                # Checking for possibilty of code:
                if len(currentValue) > 3:
                    lang = currentValue.capitalize()
                else:
                    try:
                        lang = languages.langCode(currentValue.lower())
                    except:
                        print("Language code error [Error 404: Code not found]")
                        quit(404)
                
            elif currentArgument in ("-x", "--Extension"):
                ext = currentValue.lower()

            elif currentArgument in ("-o", "--Output"): 
                out = currentValue.replace(" ", "_")
                out = out.rstrip("_")

    except getopt.error as err:
        print (str(err))
        quit()

    main(title, lang, ext, out)

#======================================================================================================================

commandLine()