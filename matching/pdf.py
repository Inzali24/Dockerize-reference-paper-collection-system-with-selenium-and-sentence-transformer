import PyPDF2
import re
pdf_file = open('D:/thesisforPdfReader.pdf', 'rb')
# pdf_file = open('https://www.academia.edu/download/62928981/F080203293320200412-55846-5e42bs.pdf','rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
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

    # if abstract_match:
    #     abstract = abstract_match.group(1).strip()
    #     print(f'The abstract on page {page_num+1} is: {abstract}')

