import PyPDF2
import re


words = ''
# Open the PDF file in binary mode
with open('D:/thesisforPdfReader.pdf', 'rb') as pdf_file:
    
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # Define the keyword to search for
    keyword = 'key words'
    
    # Define the regular expression pattern to search for
    pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format(keyword), re.IGNORECASE | re.DOTALL)
    
    # Loop through each page in the PDF file
    for page_num in range(len(pdf_reader.pages)):
        
        # Get the text of the current page
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        
        # Search for the regular expression pattern in the page text
        match = pattern.search(page_text)
        
        # If a match is found, extract the words and print them
        if match:
            words = match.group(1)
            # print(f'Page {page_num+1}: Found "{keyword}" followed by "{words}"')
    
print(words)
# Split the string into a list of substrings based on the comma delimiter
my_list = words.split(',')

# Print the resulting list


