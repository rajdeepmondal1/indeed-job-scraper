# Importing Necessary Libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import random
import os

# Path to chromedriver, setting it up
service = Service('your_path_to/chromedriver.exe')
options = webdriver.ChromeOptions()  # .FirefoxOptions()
driver = webdriver.Chrome(service=service, options=options)  # .Firefox(service=service, options=options)

# Job titles to scrape
job_titles = ['Data Scientist', 'Machine Learning Engineer', 'Data Science Consultant', 'Data Engineer', 'Data Analyst']
count = 0

# Loop through each job title
for job_title in job_titles:
    # Move to the next page automatically
    for i in range(0, 500, 10):
        # Delay to behave like a human
        time.sleep(random.randint(9, 15))
        try:
            # Website link configured to suit 'https://in.indeed.com'
            driver.get(f'https://in.indeed.com/jobs?q={job_title}&l=India&start=' + str(i))
            driver.implicitly_wait(4)
        except:
            pass

        for job in driver.find_elements(By.CLASS_NAME, 'result'):
            try:
                # Get the inner HTML
                soup = BeautifulSoup(job.get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                # Get Links of job listings to explore
                url = job.get_attribute('href')
            except StaleElementReferenceException as Exception:
                break

            # Delay to behave like a human
            time.sleep(random.randint(9, 15))

            # Open a new window
            driver.execute_script("window.open('');")
            time.sleep(random.randint(9, 15))

            # Switch to the new window
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(random.randint(9, 15))

            # Open the website in the new window
            driver.get(url)

            try:
                # Extract title from HTML
                title_soup = BeautifulSoup(driver.find_element(By.CLASS_NAME, 'jobsearch-JobInfoHeader-title-container')
                                           .get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                # Extract subtitle and company location from the HTML
                company_location_soup = BeautifulSoup(
                    driver.find_element(By.CLASS_NAME, 'jobsearch-JobInfoHeader-subtitle')
                        .get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                description_soup = BeautifulSoup(driver.find_element(By.CLASS_NAME, 'jobsearch-jobDescriptionText')
                                                 .get_attribute('innerHTML'), 'html.parser')
            except:
                pass

            try:
                # Extract Job Description from the Processed HTML
                title_soup.extend([company_location_soup, description_soup])
            except:
                pass
            time.sleep(random.randint(9, 15))

            # Make a new directory in your PC for each Job titles
            if not os.path.exists(f'{job_title}'):
                os.mkdir(f'{job_title}')

            # Write the new File
            with open(f"{job_title}/{count}.html", "w", encoding='utf-8') as file:
                file.write(str(title_soup.prettify()))
            count += 1

            # Close the current window
            driver.close()

            # Switch to the Main Window
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.randint(9, 15))

            try:
                job.click()
            except:
                pass
