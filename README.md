# pdf_to_json

Python module to Convert a  PDF file to a JSON format

The goal is to be able to quickly extract all the available information in the document to a python dictionay. The dictionay can then be stored in a database or a csv file (for a later Machine Learning processing).

The extracted information can be :
* Document metadata : title, format, version, creation date, author
* Page images
* Page texts (in Unicode, when availabe, no OCR here) and text attributes (fonts etc)

This tool uses the excellent [poppler](https://poppler.freedesktop.org/) library. 

This tool is initially intended for multilingual PDF document processing. The following tests describve the use case :

https://github.com/antoinecarme/pdf_to_json_tests/tree/master/data/multilingual

## Demo

[also availabe as a jupyter notebook](doc/prototyping_test.ipynb)

```Python
import pdf_to_json as p2j
import json

# web document : UDHR
url = "https://www.ohchr.org/EN/UDHR/Documents/UDHR_Translations/eng.pdf"

# Convert the document into a python dictionary
lConverter = p2j.pdf_to_json.pdf_to_json_converter()
lDict = lConverter.convert(url)

print(json.dumps(lDict, indent=4))

```

## Installation

pip install --upgrade git+git://github.com/antoinecarme/pdf_to_json.git
