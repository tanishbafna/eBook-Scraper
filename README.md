# eBook Scraper

The application scrapes online repositories such as Libgen, OpenLibrary, Z-Libarary and Memory of the World (in that order) to return eBooks matching the input title or author. The user can select a particular item in the output list to download the eBook and place it in their root directory.

The code can even filter out books of particular languages and extensions if required. To see a list of supported languages, take a look at the `v1_languages.py` file.

Supports the following extensions:
* `pdf`
* `txt`
* `epub`
* `mobi`

## Requirements

1. Before running the code please change the download directory in `v1_downloadFin.py`, otherwise python will raise an error.
2. Install requirements by running `pip3 install -r requirements.txt`
3. Chromedriver matching your current Google Chrome version is required for `Selenium` to download books from Z-Library. Books from all other databases are downloaded using `requests` and `BeautifulSoup4`.

## Running the Code

Run `book.py` from the command line with the arguments structured according to one of the following formats:

1. `python3 book.py [title]`
2. `python3 book.py [title] -l [language code] -x [extension] -o [output file name]`

`-l` and `-x` are optional arguments which help to filter the results. If `-o [output file name]` is included, the downloaded book will be saved as `output file name`. Do not include any extension in this argument.

### Example

> python3 book.py sapiens -l eng -x epub -o sap_ebook

Although simply running `book.py` works, the application can also be converted into a command line tool by saving it as an executable script.