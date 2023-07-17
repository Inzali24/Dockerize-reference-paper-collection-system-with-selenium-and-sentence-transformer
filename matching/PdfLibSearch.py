
import io
import requests
from PyPDF2 import PdfReader
import re
r = requests.get("https://www.academia.edu/download/53797460/IRJET-V4I6500.pdf")
f = io.BytesIO(r.content)
try:
 pdf_reader = PdfReader(f, strict = False)
 pass
except Exception as e:
 print(e)
      
  # Define the keyword to search for
keywords = ['Index Terms','keywords']
matched_keyword=''
# Define the regular expression pattern to search for
# pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format('|'.join(keywords)), re.IGNORECASE | re.DOTALL)
page_text=""
for page_num in range(len(pdf_reader.pages)):    
# Get the text of the current page
 page = pdf_reader.pages[page_num]
 page_text+= page.extract_text()

paragraph=""
for keyword in keywords: 
 pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format(keyword), re.IGNORECASE | re.DOTALL)
  
 match = pattern.search(page_text)
 # If a match is found, extract the words and print them
 if match:
   paragraph = match.group(0)
   matched_keyword=keyword
 else:
   paragraph = "No matching paragraph found."

 paragraph = ''.join(paragraph)
 print(paragraph)