# pdf_to_json
Python module to Convert a  PDF file to a JSON format

The goal is to be able to quickly extract all the available information in the document to a python dictionay. The dictionay can then be stored in a database or a csv file (for a later Machine Learning processing).

The extracted information can be :
* Document metadata : title, format, versino, creation date, author
* Page images
* Page texts (in Unicode) and attirbutes (fonts etc)

This tool uses the excellent [poppler](https://poppler.freedesktop.org/)  library. It is initially intended for multilingual PDF document processing.
