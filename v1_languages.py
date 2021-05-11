#!/usr/bin/env python
#======================================================================================================================

languages = {

"eng":"English",
"en":"English",
"es":"Spanish",
"spa":"Spanish",
"fr":"French",
"fre":"French",
"de":"German",
"ger":"German",
"hi":"Hindi",
"hin":"Hindi",
"ur":"Urdu",
"urd":"Urdu",
"bn":"Bengali",
"ben":"Bengali",
"mr":"Marathi",
"mar":"Marathi",
"zh":"Chinese",
"chi":"Chinese",
"ru":"Russian",
"rus":"Russian",
"it":"Italian",
"ita":"Italian",
"ja":"Japanese",
"jpn": "Japanese",
"ar":"Arabic",
"ara":"Arabic",
"ko":"Korean",
"kor":"Korean",
"la":"Latin",
"lat":"Latin"

}

#======================================================================================================================

# Returns language code.
def openlib_langCode(full):

    for key, val in languages.items():

        if val == full and len(key) > 2:
            return key

#======================================================================================================================

# Returns full language.
def langCode(short):

    return languages[short]

#======================================================================================================================
