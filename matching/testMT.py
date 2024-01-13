import concurrent.futures
import time
import machinelearn
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def scrape_data(url, keywords):
    # Initialize a new Selenium WebDriver
    op = webdriver.ChromeOptions()
    #add option
    op.add_argument('--headless')
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-setuid-sandbox") 
    op.add_argument('--disable-dev-shm-usage')  
    #driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
    
    driver = webdriver.Chrome(options=op)
    try:
        # Navigate to the URL
        driver.get(url)
        div_elements = driver.find_elements(By.CLASS_NAME, "gs_r.gs_or.gs_scl")
        pdf_links = []
        citations = []
        lst=[]
        title = []
        for div_element in div_elements:
          # Check if there are any [PDF] spans within gs_ri
          gs_ri = div_element.find_element(By.CLASS_NAME, "gs_ri")
          pdf_spans_gs_ri = gs_ri.find_elements(By.XPATH, './/span[contains(text(), "[PDF]")]')
          
          if pdf_spans_gs_ri:
            try:        
              pdf_link =div_element.find_element(By.PARTIAL_LINK_TEXT, "PDF").get_attribute("href")
              title = gs_ri.find_element(By.TAG_NAME, "a").text
              citation_a = gs_ri.find_element(By.XPATH, ".//a[contains(@href, 'cites=')]")
              citations = int(citation_a.text.split()[-1])
              pdf_links.append({"title": title, "pdf_link": pdf_link, "citations": citations})                    
            except Exception as e:
               print(e)
          else:
              try:
                gs_ggsd = WebDriverWait(div_element, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "gs_ggsd")))
                pdf_spans_gs_ggsd = gs_ggsd.find_elements(By.XPATH, './/span[contains(text(), "[PDF]")]')        
                if pdf_spans_gs_ggsd:
                  pdf_link = gs_ggsd.find_element(By.PARTIAL_LINK_TEXT, "PDF").get_attribute("href")
                  title = gs_ri.find_element(By.TAG_NAME, "a").text
                  citation_a = gs_ri.find_element(By.XPATH, ".//a[contains(@href, 'cites=')]")
                  citations = int(citation_a.text.split()[-1])
                  pdf_links.append({"title": title, "pdf_link": pdf_link, "citations": citations}) 
              except Exception as e:
               print(e)
          
        if pdf_links:
           for item in pdf_links:
              similarity = machinelearn.getlist(item["pdf_link"], keywords)
              if similarity != 0:
                absolute=abs(int(float(similarity)*450)) 
                if type(similarity)==bool:  
                   absolute=random.randint(10, 30)
                lst.append({'title':item["title"],'url':item["pdf_link"],'similarity': absolute,'citations':item["citations"]})
        
        driver.close() 
        return lst
    finally:
        # Close the WebDriver to free up resources
        driver.quit()

def RunAutomation(title, keywords): 
    # List of URLs to scrape
    #op = webdriver.ChromeOptions()
    op = webdriver.ChromeOptions()
    #add option
    op.add_argument('--headless')
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-setuid-sandbox") 
    op.add_argument('--disable-dev-shm-usage')  
    driver = webdriver.Chrome(options=op)
    
    try:
       driver.get('https://scholar.google.com/') 
       search_box = driver.find_element(By.NAME, "q")
       #search_box.send_keys('selenium webdriver')
       search_box.send_keys(title)
       search_box.submit()
       link=[]
       i=1
       result = []
       start = time.time()
       while(i<10):
         # Find all the relevant div elements 
         i = i + 1
         link_url=driver.find_element(By.LINK_TEXT,str(i)).get_attribute("href")
         link.append(link_url)
       driver.find_element(By.LINK_TEXT,str(2)).click()
       link_url=driver.find_element(By.LINK_TEXT,str(1)).get_attribute("href")
       link.insert(0,link_url)
       
       # Use concurrent.futures.ThreadPoolExecutor for multi-threading
       with concurrent.futures.ThreadPoolExecutor() as executor:
           # Pass the URLs to the executor.map function for parallel processing
           results = list(executor.map(scrape_data, link, keywords))
   
       # Process the results as needed
       for result_list in results:
           for result_dict in result_list:
               result.append(result_dict)
      
       end = time.time() 
       print(f"Time taken for multithreaded scraper: {end - start} seconds")
       sorted_data = sorted(result,  key=lambda x: x["similarity"], reverse=True)
       return sorted_data
    finally:
        # Close the WebDriver instance to release resources
        driver.quit()
    

