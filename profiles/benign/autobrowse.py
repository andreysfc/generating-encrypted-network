#!/usr/bin/env python
# Automatic browsing random websites using Selenium Python
# Author: Andrey Ferriyan <andrey@sfc.wide.ad.jp>
# Script: autobrowse.py
# v1.0
#
# Configuration for production use,
# HEADLESS=1, DEBUG=0


from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from threading import Thread
import time
import pandas as pd
import selenium

DEBUG=0
HEADLESS=1
SAMPLE=10000
WAITING_TIME=5
START_SAMPLE=10
STOP_SAMPLE=15
PROXY=1
THREADS=5
threads = []

FIREFOX_DRIVER="../../aux/firefox/geckodriver"
CHROME_DRIVER="../../aux/chrome/chromedriver"
TOPWEBSITES="../../raw_data/sites/top-1m.csv"

# mitmproxy configuration
ourProxy = "localhost:8080"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
	'proxyType': "MANUAL",
	'httpProxy': ourProxy,
	'ftpProxy': ourProxy,
	'sslProxy': ourProxy,
}
webdriver.DesiredCapabilities.CHROME['proxy'] = {
        'proxyType': "MANUAL",
        'httpProxy': ourProxy,
        'ftpProxy': ourProxy,
        'sslProxy': ourProxy,
}


# browsers configuration
chrome_opt = webdriver.ChromeOptions()
firefox_opt = webdriver.FirefoxOptions()

if HEADLESS == 1 and PROXY == 1:
   chrome_opt.add_argument("--headless")
   firefox_opt.add_argument("--headless")


#load the data
df = pd.read_csv(TOPWEBSITES)

# random sampling websites
samples = df.sample(n=SAMPLE)

print("{}".format(samples))

with webdriver.Firefox(executable_path=FIREFOX_DRIVER,options=firefox_opt) as f_driver:
	for idx, iurl in zip(samples['index'], samples['url']):
		try:
		   f_links = []
		   f_driver.get("https://"+iurl)
		   f_elem = f_driver.find_elements_by_tag_name("a")
		   for elx in f_elem:
		      href = elx.get_attribute("href")
		      f_links.append(href)
		   f_getPartial = f_links[START_SAMPLE:STOP_SAMPLE]
		   for idx, ilink in enumerate(f_getPartial):
		      print("{}".format(ilink))
		      f_driver.get(ilink)
		      time.sleep(WAITING_TIME)
		except selenium.common.exceptions.InvalidArgumentException:
		   continue
		except selenium.common.exceptions.WebDriverException:
		   continue

f_driver.quit()

with webdriver.Chrome(executable_path=CHROME_DRIVER,options=chrome_opt) as c_driver:
	for idy, jurl in zip(samples['index'], samples['url']):
		try:
		   c_links = []
		   c_driver.get("https://"+jurl)
		   c_elem = c_driver.find_elements_by_tag_name("a")
		   for ely in c_elem:
		      href = ely.get_attribute("href")
		      c_links.append(href)
		   c_getPartial = c_links[START_SAMPLE:STOP_SAMPLE]
		   for idy, jlink in enumerate(c_getPartial):
		      print("{}".format(jlink))
		      c_driver.get(jlink)
		      time.sleep(WAITING_TIME)
		except selenium.common.exceptions.InvalidArgumentException:
		   continue
		except selenium.common.exceptions.WebDriverException:
		   continue

c_driver.quit()
