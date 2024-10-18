import io
import requests
from PyPDF2 import PdfReader
from requests.exceptions import SSLError
import re
import random
import urllib3
import logging 
words = ''

def getlist(url,keyword):
  try:
    text =''
    #url = 'https://arxiv.org/pdf/2402.01480'
    logging.basicConfig(level=logging.INFO)
    r = requests.get(url)
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": url
   }

    response = requests.get(url, headers=headers)
    
    response.raise_for_status()  # Check for other request errors (optional)
    urllib3.disable_warnings()
    # Check if the Content-Type header indicates a PDF
    #content_type = response.headers.get("Content-Type", "")
    #is_pdf = content_type.lower().startswith("application/pdf")   
    #if not is_pdf:         
      #return 'pdf' in url.lower() if random.uniform(0.05, 0.08) else 0
      #return 0
    #else:
      # Create a PDF reader object
    f = io.BytesIO(r.content)
    try:
      pdf_reader = PdfReader(f)
      pass
    except Exception as e:
      return 0
      
    # Define the keyword to search for
    if len(pdf_reader.pages) > 100:
      return 0
    # Loop through each page and extract text
    for page_num in range(len(pdf_reader.pages)):  
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
       # Search for the abstract section
    start_index = text.lower().find("abstract")
    if start_index == -1:
      return 0
    # Extract the abstract paragraph
    abstract_text = text[start_index:]
    # Define potential end markers
    end_markers = ["keywords", "index terms", "key words", "introduction"]
    logging.info('sentence1 user abstract', 'step2')
    # Find the earliest occurrence of any end marker
    end_indices = [abstract_text.lower().find(marker) for marker in end_markers if abstract_text.lower().find(marker) != -1]
    # Get the earliest end marker if found, otherwise use the full text
    if end_indices:
        end_index = min(end_indices)
    else:
         end_index = len(abstract_text)
    # Return the abstract text up to the earliest end marker
    abstract_paragraph = abstract_text[:end_index].strip()
    if not abstract_paragraph: 
       return 0
      
    logging.basicConfig(level=logging.INFO)
    logging.info('response sentence1', keyword)
    logging.info('response sentence2', abstract_paragraph)
    API_KEY = 'Please get your api key from hugging face'
    # Define the endpoint and headers
    API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {API_KEY}"}
   # Prepare input data
    data = {
        "inputs": {
        "source_sentence": keyword,
        "sentences": [abstract_paragraph]
      }
    }
    # Send the request to the API
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    logging.info('response result', f"Similarity: {result[0] * 100:.2f}")
    return result[0] # Similarity score      
  except SSLError as e:
    return 0 
  except requests.exceptions.RequestException as e:
    # Handle other request-related exceptions
    #return random.uniform(0.05, 0.08)
    return e.response.status_code
  except Exception as e:
      # Handle other unexpected exceptions
      return 0    


    
  
