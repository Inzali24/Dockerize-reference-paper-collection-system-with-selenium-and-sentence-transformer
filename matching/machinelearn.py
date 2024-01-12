import io
import requests
from PyPDF2 import PdfReader
from requests.exceptions import SSLError
import re
import urllib3
from sentence_transformers import SentenceTransformer, util
url = 'https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=65e283a565b98fc8d3e6aa4069f13ea32dda9a03'
words = ''

def getlist(url,keyword):
  try:
    r = requests.get(url,verify=False)
    response = requests.head(url)
    response.raise_for_status()  # Check for other request errors (optional)
    urllib3.disable_warnings()
    # Check if the Content-Type header indicates a PDF
    content_type = response.headers.get("Content-Type", "")
    is_pdf = content_type.lower().startswith("application/pdf")   
    if not is_pdf or response.status_code == 404:
      print("The URL does not point to a PDF file.") 
      return ''
    else:
      print("The URL points to a PDF file.")
      # Create a PDF reader object
      f = io.BytesIO(r.content)
      try:
        pdf_reader = PdfReader(f, strict = False)
        pass
      except Exception as e:
        print(e,url)
        return ''
        
      # Define the keyword to search for
      keywords = ['Index Terms','keywords', 'Key Words']
      matched_keyword = ''
      # Define the regular expression pattern to search for
      # pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format('|'.join(keywords)), re.IGNORECASE | re.DOTALL)
      page_text = ""
      for page_num in range(len(pdf_reader.pages)):  
      # Get the text of the current page
       page = pdf_reader.pages[page_num]
       page_text+= page.extract_text()
  
      paragraph=""
      for w in keywords: 
        pattern = re.compile(r'\b{}\b\s+(.*?[.?!])'.format(w), re.IGNORECASE | re.DOTALL)
    
        match = pattern.search(page_text)
      # If a match is found, extract the words and print them
        if match:
          paragraph = match.group(0)
          matched_keyword=w
          break
      
      if paragraph =="":
        return ''
      
      paragraph = ''.join(paragraph)
      print(paragraph)
      
  
      new_sentence = paragraph.replace(matched_keyword, '')
      print('here is keywords extracted from pdf',new_sentence)
      sentences1 = keyword.split()
  
      #sentences1 = ['Automation, Open Source, Selenium, Testing Tools, Web Driver']
  
      sentences2 = [new_sentence]
  
      model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
  
      #Compute embedding for both lists
      embedding_1= model.encode(sentences1, convert_to_tensor=True)
      embedding_2 = model.encode(sentences2, convert_to_tensor=True)
  
      cosine_scores =util.cos_sim(embedding_1, embedding_2)
      #Output the pairs with their score
      print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[0], sentences2[0], cosine_scores[0][0]))
      similarity = cosine_scores[0][0].item()
      percentageSim = "{:.2}".format(similarity)  
      return percentageSim
  except SSLError as e:
    # Handle SSL errors
    print("SSL Error:", e) 
    return '' 
  except requests.exceptions.RequestException as e:
    # Handle other request-related exceptions
    print("Request Exception:", e)
    return ''
  except Exception as e:
      # Handle other unexpected exceptions
      print("Unexpected Exception:", e)
      return '' 

    
  
