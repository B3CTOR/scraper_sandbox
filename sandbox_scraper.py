from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(r'C:\chromedriver.exe', options = options)
driver.get("http://books.toscrape.com/")
titles = []
prices = []
page = 1
next_value = 2
while page < 50:
	n = 0
	try:
		for i in range(20):
			n += 1
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[' + str(n) + ']/article/div[1]/a/img')))
			book = driver.find_element_by_xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li[' + str(n) + ']/article/div[1]/a/img').click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
			title = driver.find_element_by_tag_name('h1')
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'price_color')))
			price = driver.find_element_by_class_name('price_color')
			titles.append(title.text)
			prices.append(price.text)
			driver.get("http://books.toscrape.com/catalogue/page-{}.html".format(str(page)))
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	except:
		print('')
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[3]/a')))
		time.sleep(2)
		next_button = driver.find_element_by_xpath('//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[3]/a').click()
		page += 1
		next_value = next_value + 1
	except:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[2]/a')))
		time.sleep(2)
		next_button = driver.find_element_by_xpath('//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li[2]/a').click()
		page += 1
		next_value = next_value + 1

df = pd.DataFrame({'Title':titles, 'Prices':prices})

df.to_excel('Scraping Sandbox.xlsx', index = False)
