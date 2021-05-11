#!/usr/bin/env python
#======================================================================================================================

import requests                                             # For downloading file
import subprocess                                           # For opening final product
from tqdm import tqdm                                       # For displaying download bar

#======================================================================================================================

DownloadPath = '/Users/tanishbafna/Downloads'

def BookDownloader(link, downloadLocation):

    # Downloading:
    try:
        downloadBook = requests.get(link, stream = True)
    except:
        print("DOWNLOADING ERROR")
        return 404, 404

    downloadLocation = DownloadPath + downloadLocation

    # Progress bar:
    totalSize = int(downloadBook.headers.get('content-length', 0))
    blockSize = 1024
    tqdmDownload = tqdm(total = totalSize, unit = 'iB', unit_scale = True, desc = "Downloading... ", bar_format = '{l_bar}{bar:30}{r_bar}{bar:-30b}')

    with open(downloadLocation, "wb") as f:
        for data in downloadBook.iter_content(blockSize):
            tqdmDownload.update(len(data))
            f.write(data)

    tqdmDownload.close()

    print("")
    if totalSize != 0 and tqdmDownload.n != totalSize:
        return print("DOWNLOADING ERROR")

    # Opening the book using default application:
    print("Opening the book...\n")
    return subprocess.run(['open', downloadLocation], check = True)

#======================================================================================================================