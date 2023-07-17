import time
import machinelearn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def RunAutomation(keywords): 
 driver = webdriver.Chrome(executable_path='C:\\Users\\Inzali Naing\\matching\\chromedriver.exe')
 driver.get('https://scholar.google.com/') 
 search_box = driver.find_element(By.NAME, "q")
 #search_box.send_keys('selenium webdriver')
 search_box.send_keys(keywords)
 search_box.submit()
 lst=[]
 i=1
# div = driver.find_element(By.ID,"gs_nml")
# for a_element in div.find_elements(By.TAG_NAME,'a'):
 index=0;
 while(i<11):
   for div_element in driver.find_elements(By.CLASS_NAME,"gs_ri"):    
     pdf_spans = div_element.find_elements(By.XPATH,'.//span[contains(text(), "[PDF]")]')
     if pdf_spans:
      a_element = div_element.find_element(By.TAG_NAME,'a')
      # print("Link URL:", a_element.get_attribute("href"))
      # print("Link text:", a_element.text)
      title = a_element.text
      url = a_element.get_attribute("href")
      similarity = machinelearn.getlist(url,keywords)
      index=index+1
      lst.append({'No':index,'title':title,'url':url,'similarity': similarity})
      # if similarity is not None:
         
   i=i+1
   driver.find_element(By.LINK_TEXT,str(i)).click()
 driver.quit() 
 return lst;
  


# for div_element in driver.find_elements(By.CLASS_NAME,"gs_ri"):    
#     pdf_spans = div_element.find_elements(By.XPATH,'.//span[contains(text(), "[PDF]")]')
#     if pdf_spans:
#      a_element = div_element.find_element(By.TAG_NAME,'a')
#      print("Link URL:", a_element.get_attribute("href"))
#      print("Link text:", a_element.text)




# for elem in driver.find_elements(By.XPATH,"//span[contains(@class, 'gs_ct1')]" ):
#     print(elem.text,"jjjj")       
    # if elem.text == "[PDF]":
    #     title = driver.find_element(By.TAG_NAME,"")

# try:
#     div_element = driver.find_element_by_class_name("gs_ri")
#     pdf_spans = div_element.find_elements_by_xpath('.//span[contains(text(), "[PDF]")]')
#     if pdf_spans:
#         a_element = div_element.find_element_by_tag_name("a")
#         print("Link URL:", a_element.get_attribute("href"))
# except NoSuchElementException:
#     print("Element not found")
# finally:
#     print("quit")
#     driver.quit()

    
# div_element = driver.find_element_by_class_name("gs_ri")
# print(div_element)
# pdf_spans = div_element.find_elements_by_xpath('.//span[contains(text(), "[PDF]")]')
# if pdf_spans:
#     a_element = div_element.find_element_by_tag_name("a")
#     print("Link URL:", a_element.get_attribute("href"))

# keywords="selenium webdriver"

# RunAutomation(keywords)