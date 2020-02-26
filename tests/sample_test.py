

import pdf_to_json as p2j

# web document : UDHR
url = "https://www.ohchr.org/EN/UDHR/Documents/UDHR_Translations/eng.pdf"

# Convert the document into a python dictionary
lConverter = p2j.pdf_to_json.pdf_to_json_converter()
lDict = lConverter.convert(url)

print(lDict)
