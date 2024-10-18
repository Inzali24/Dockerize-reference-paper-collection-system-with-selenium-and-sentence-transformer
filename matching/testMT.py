import concurrent.futures
import time
import machinelearn
import random
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging

keyword_from_user =''
def scrape_data(url):
    # Initialize a new Selenium WebDriver
    global keyword_from_user
    op = webdriver.ChromeOptions()
    #add option
    op.add_argument('--headless')
    op.add_argument('--disable-blink-features=AutomationControlled')
    op.add_argument('--diable-popup-blocking')
    op.add_argument('--start-maximized')
    # disable extensions
    op.add_argument('--disable-extensions')
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-setuid-sandbox") 
    op.add_argument('--disable-dev-shm-usage')  
    driver = webdriver.Chrome(options=op)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    op.add_argument(f'user-agent={user_agent}')
    
    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    #enable stealth mode
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
           )

    #driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
    logging.basicConfig(level=logging.INFO)
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
        logging.info('pdf_links',pdf_links)
        if pdf_links:
           for item in pdf_links:              
              similarity = machinelearn.getlist(item["pdf_link"], keyword_from_user)   
              if similarity>100:
                similarity=0
              logging.info('without formatting ',similarity)
              absolute=int(similarity*100)
              lst.append({'title':item["title"],'url':item["pdf_link"],'similarity': absolute,'citations':item["citations"]})
              # if similarity != 0:
              #   absolute=abs(int(float(similarity)*500))
              #   if type(similarity)==bool:  
              #      absolute=random.randint(10, 35)
              #   lst.append({'title':item["title"],'url':item["pdf_link"],'similarity': absolute,'citations':item["citations"]})
        
        driver.close() 
        return lst
    finally:
        # Close the WebDriver to free up resources
        driver.quit()

def RunAutomation(title, keywords): 
    # List of URLs to scrape
    global keyword_from_user
    keyword_from_user= keywords
    op = webdriver.ChromeOptions()
    #add option
    op.add_argument('--headless')
    op.add_argument('--disable-blink-features=AutomationControlled')
    op.add_argument('--diable-popup-blocking')
    op.add_argument('--start-maximized')
    # disable extensions
    op.add_argument('--disable-extensions')
    op.add_argument('--no-sandbox')
    op.add_argument("--disable-setuid-sandbox") 
    op.add_argument('--disable-dev-shm-usage')  
    driver = webdriver.Chrome(options=op)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    user_agents = [
    # Add your list of user agents here
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    op.add_argument(f'user-agent={user_agent}')
    
    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    #enable stealth mode
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
           )

    try:
       driver.get('https://scholar.google.com/')
       search_box = driver.find_element(By.NAME, "q")
       #search_box.send_keys('selenium webdriver')
       logging.basicConfig(level=logging.INFO)
       search_box.send_keys(title)
       search_box.submit()
       link=[]
       i=1
       result = []
       start = time.time()
       while(i<3):
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
           results = list(executor.map(scrape_data, link))
   
       # Process the results as needed
       for result_list in results:
           for result_dict in result_list:
               result.append(result_dict)
      
       end = time.time()
       print(f"Time taken for multithreaded scraper: {end - start} seconds")
       sorted_data = sorted(result, key=lambda x: x["similarity"], reverse=True)
       return sorted_data
    finally:
        # Close the WebDriver instance to release resources
        driver.quit()
    

