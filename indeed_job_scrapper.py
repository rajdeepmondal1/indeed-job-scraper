from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd 
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import os

service = Service('your_path_to/chromedriver.exe')
options = webdriver.ChromeOptions() # .FirefoxOptions()
driver = webdriver.Chrome(service=service, options=options) #.Firefox(service=service, options=options)

job_titles = ['Data Scientist', 'Machine Learning Engineer', 'Data Science Consultant', 'Data Engineer', 'Data Analyst'] 
count = 0
for job_title in job_titles:  
    for i in range(0,500,10):
        time.sleep(random.randint(9, 15)) 
        try:
            driver.get(f'https://in.indeed.com/jobs?q={job_title}&l=India&start='+str(i))
            driver.implicitly_wait(4)  
        except:
            pass

        for job in driver.find_elements(By.CLASS_NAME, 'result'):
            try:
                soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                url = job.get_attribute('href')
            except StaleElementReferenceException as Exception:
                break                   

            time.sleep(random.randint(9, 15))
            driver.execute_script("window.open('');")
            time.sleep(random.randint(9, 15))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.randint(9, 15))
            driver.get(url)    

            try:
                title_soup = BeautifulSoup(driver.find_element(By.CLASS_NAME, 'jobsearch-JobInfoHeader-title-container')
                                     .get_attribute('innerHTML'), 'html.parser')    
            except:
                pass

            try:
                company_location_soup = BeautifulSoup(driver.find_element(By.CLASS_NAME, 'jobsearch-JobInfoHeader-subtitle')
                                     .get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                description_soup = BeautifulSoup(driver.find_element(By.CLASS_NAME, 'jobsearch-jobDescriptionText')
                                     .get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                title_soup.extend([company_location_soup, description_soup])
            except:
                pass
            time.sleep(random.randint(9, 15))
            
            if not os.path.exists(f'{job_title}'):
                os.mkdir(f'{job_title}')
                
            with open(f"{job_title}/{count}.html", "w", encoding = 'utf-8') as file:
                file.write(str(title_soup.prettify()))        
            count += 1

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.randint(9, 15))        

            try:
                job.click()
            except:
                pass 