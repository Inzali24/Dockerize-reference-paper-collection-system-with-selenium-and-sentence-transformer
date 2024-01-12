import time
import machinelearn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
def RunAutomation(title, keywords): 
 
 #driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\matching\\chromedriver.exe')
 #service = Service(executable_path=r'/usr/local/bin/chromedriver') 
 op = webdriver.ChromeOptions()
 #add option
 op.add_argument('--headless')
 op.add_argument('--no-sandbox')
 op.add_argument("--disable-setuid-sandbox") 
 driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
 driver = webdriver.Chrome(options=op)
    
 driver.get('https://scholar.google.com/') 
 search_box = driver.find_element(By.NAME, "q")
 #search_box.send_keys('selenium webdriver')
 search_box.send_keys(title)
 search_box.submit()
 lst=[]
 i=1
# div = driver.find_element(By.ID,"gs_nml")
# for a_element in div.find_elements(By.TAG_NAME,'a'):
 while(i<11):
   # Find all the relevant div elements
  div_elements = driver.find_elements(By.CLASS_NAME, "gs_r.gs_or.gs_scl")

  pdf_links = []
  citations = []
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
        print(f"Cited by: {citations}")
        pdf_links.append({"title": title, "pdf_link": pdf_link, "citations": citations})                    
      except Exception as e:
         print("Element1 not found:", e)
    else:
        try:
          gs_ggsd = WebDriverWait(div_element, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "gs_ggsd")))
          pdf_spans_gs_ggsd = gs_ggsd.find_elements(By.XPATH, './/span[contains(text(), "[PDF]")]')        
          if pdf_spans_gs_ggsd:
            pdf_link = gs_ggsd.find_element(By.PARTIAL_LINK_TEXT, "PDF").get_attribute("href")
            title = gs_ri.find_element(By.TAG_NAME, "a").text
            citation_a = gs_ri.find_element(By.XPATH, ".//a[contains(@href, 'cites=')]")
            citations = int(citation_a.text.split()[-1])
            print(f"Cited by: {citations}")
            pdf_links.append({"title": title, "pdf_link": pdf_link, "citations": citations}) 
        except Exception as e:
         print("Element2 not found:", e)
    
  # If gs_ri or gs_ggsd has PDF, print the titles and PDF links
  if pdf_links:
     print("PDF links found:")
     for item in pdf_links:
        print("Title:", item["title"])
        print("PDF Link:", item["pdf_link"])
        print("citations:", item["citations"])
        similarity = machinelearn.getlist(item["pdf_link"],keywords)
        if similarity != '':        
         lst.append({'title':item["title"],'url':item["pdf_link"],'similarity': float(similarity)*100,'citations':item["citations"]})
  else:
      print("No PDF links found.")
  i = i + 1
  driver.find_element(By.LINK_TEXT,str(i)).click()
 driver.quit()
 print(lst)
 sorted_data = sorted(lst,  key=lambda x: x["similarity"], reverse=True)
 return sorted_data;