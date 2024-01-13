import io
import requests
from PyPDF2 import PdfReader
from requests.exceptions import SSLError
import re
import urllib3
import urllib.request
from sentence_transformers import SentenceTransformer, util
words = ''

def getlist(url):
  try:
    r = requests.get(url,verify=True)
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

      if not paragraph:
         print('No Keywords')         
         percentageSim = 0.4 
         print(percentageSim)    
         return percentageSim
      
      print(f'Keyword: {matched_keyword}')
      
  
      new_sentence = paragraph.replace(matched_keyword, '')
      print('here is keywords extracted from pdf',new_sentence)
      

      #sentences1 = keyword.split()
  
      sentences1 =  ['Keywords : Software testing, Selenium, Watir, Webdriver, test automation, web-testing']
  
      sentences2 = [new_sentence]
  
      model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
  
      #Compute embedding for both lists
      embedding_1= model.encode(sentences1, convert_to_tensor=True)
      embedding_2 = model.encode(sentences2, convert_to_tensor=True)
  
      cosine_scores =util.cos_sim(embedding_1, embedding_2)
      #Output the pairs with their score
      print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[0], sentences2[0], cosine_scores[0][0]))
      similarity = cosine_scores[0][0].item()
      percentageSim = "{:.2}".format(similarity+0.5)  
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
    

def get_final_url(url):
    try:
        response = requests.head(url, allow_redirects=True)      
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def main(): 
    original_url = 'https://arxiv.org/ftp/arxiv/papers/1611/1611.00578.pdf'
    final_url = get_final_url(original_url)

    if final_url:
        if final_url != original_url:
            print(f"The URL was redirected to: {final_url}")
            
            getlist(final_url)
            # Now, you can proceed to read the PDF from the final URL using the previous example
        else:
            print("No redirection occurred.")
            getlist(original_url)
    else:
        print("Failed to determine the final URL.")

if __name__ == "__main__":
    main()