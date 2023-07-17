import requests
import io
# import PyPDF2
# import pdfplumber

#url = "https://www.academia.edu/download/62928981/F080203293320200412-55846-5e42bs.pdf"

# Send a request to the URL and get the response content
# response = requests.get(url)
# pdf_bytes = io.BytesIO(response.content)
# print(pdf_bytes)
# with pdfplumber.open(pdf_bytes) as pdf:
#     page = pdf.pages[0]
#     text = page.extract_text()
#     print(text)

# import pdfplumber


# url = "https://www.academia.edu/download/62928981/F080203293320200412-55846-5e42bs.pdf"

# rq = requests.get(url)

# pdf = pdfplumber.load(io.BytesIO(rq.content))
# text = ''
# for page in pdf.pages:
#     text += page.extract_text()
# print(text)

# import urllib3
# import pdfplumber
# import io
# def read_pdf(url: str) -> str:
#     http = urllib3.PoolManager()
#     temp = io.BytesIO()
#     temp.write(http.request("GET", url).data)
#     with pdfplumber.load(temp) as pdf:
#         text = pdf.pages[0].extract_text()
#     return text

# url = "https://www.academia.edu/download/62928981/F080203293320200412-55846-5e42bs.pdf"
# text = read_pdf(url)
# print(text)

# import fitz

# url = "https://www.academia.edu/download/62928981/F080203293320200412-55846-5e42bs.pdf"
# with fitz.open(url) as pdf_file:
#     text = ""
#     for page in pdf_file:
#         text += page.get_text()
#     print(text)

import requests
from PyPDF2 import PdfReader
import re
url = 'https://sciresol.s3.us-east-2.amazonaws.com/IJST/Articles/2017/Issue-13/Article4.pdf'

r = requests.get(url)
f = io.BytesIO(r.content)

pdf_reader = PdfReader(f)
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    page_text = page.extract_text()
   # print(page_text)
    pattern = r"Abstract[\s\S]*?(?=Introduction|$)"
    abstract_match = re.search(pattern, page_text)
    print(abstract_match)
    if abstract_match:
            abstract_text = abstract_match.group(0)
            break

if abstract_text:
    print("Abstract found:\n", abstract_text)
else:
    print("No abstract found.")
# contents = reader.pages[0].extract_text().split('\n')
# print(contents)