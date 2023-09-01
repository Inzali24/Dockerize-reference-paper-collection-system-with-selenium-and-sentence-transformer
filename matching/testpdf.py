import time
import machinelearn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def RunAutomation(title, keywords): 
 driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\matching\\chromedriver.exe')
 driver.get('https://scholar.google.com/') 
 search_box = driver.find_element(By.NAME, "q")
 #search_box.send_keys('selenium webdriver')
 search_box.send_keys(title)
 search_box.submit()
 lst=[]
 i=1
# div = driver.find_element(By.ID,"gs_nml")
# for a_element in div.find_elements(By.TAG_NAME,'a'):
 index=0;
 while(i<11):
   for div_element in driver.find_elements(By.CLASS_NAME,"gs_ri"):
     # Assuming the element with the "cites" information is the only one with an "a" tag in the page
    #  element = div_element.find_element(By.XPATH, "//a[contains(@href, 'cites=')]")
     # Extract the number from the "Cited by" text and convert it to an integer
    #  citations = int(element.text.split()[-1])
    #  print(f"Cited by: {citations}")
     citations=0
     pdf_spans = div_element.find_elements(By.XPATH,'.//span[contains(text(), "[PDF]")]')
     if pdf_spans:
      try:
        # Find the nested a tag containing "cites=" info
        citation_a = div_element.find_element(By.XPATH, ".//a[contains(@href, 'cites=')]")
        # Extract the number from the "Cited by" text and convert it to an integer
        citations = int(citation_a.text.split()[-1])
        print(f"Cited by: {citations}")
      except NoSuchElementException:
        print("No 'cites' info found for this element.")      
      a_element = div_element.find_element(By.TAG_NAME,'a')     
      title = a_element.text
      url = a_element.get_attribute("href")
      similarity = machinelearn.getlist(url,keywords)
      index=index+1
      lst.append({'No':index,'title':title,'url':url,'similarity': similarity,'citations':citations})
      # if similarity is not None:         
   i=i+1
   driver.find_element(By.LINK_TEXT,str(i)).click()
 driver.quit() 
#  lst.sort(key=lambda x: x['similarity'], reverse=True)
 return lst;