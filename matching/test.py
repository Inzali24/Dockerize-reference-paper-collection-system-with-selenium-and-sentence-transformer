import time
import machinelearn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def RunAutomation(title,keywords): 
 driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\matching\\chromedriver.exe')
 driver.get('https://scholar.google.com/') 
 search_box = driver.find_element(By.NAME, "q")
 #search_box.send_keys('selenium webdriver')
 search_box.send_keys(title)
 search_box.submit()
 lst=[]
 i=1
 index=0
# div = driver.find_element(By.ID,"gs_nml")
# for a_element in div.find_elements(By.TAG_NAME,'a'):
 for div_element in driver.find_elements(By.XPATH, "//div[contains(@class, 'gs_ri') and .//span[contains(text(), 'PDF')]]"):
   #pdf_spans = div_element.find_elements(By.XPATH,'.//span[contains(text(), "[PDF]")]')
   #print('before',div_element)
   #if pdf_spans:
   citation_a = div_element.find_element(By.XPATH, ".//a[contains(@href, 'cites=')]")
   # Extract the number from the "Cited by" text and convert it to an integer
   citations = int(citation_a.text.split()[-1])
   print(f"Cited by: {citations}")
   a_element = div_element.find_element(By.TAG_NAME,'a')
   # print("Link URL:", a_element.get_attribute("href"))
   # print("Link text:", a_element.text)
   title = a_element.text
   url = a_element.get_attribute("href")
   similarity = machinelearn.getlist(url,keywords)
   index=index+1
   lst.append({'No':index,'title':title,'url':url,'similarity': similarity,'citation': citations})
   # if similarity is not None:         
 driver.quit() 
 print(lst)
#  lst.sort(key=lambda x: x['similarity'], reverse=True)
 return lst;

RunAutomation("selenium webdriver", "selenium webdriver, webdriver IDE, python, frontend, testing")