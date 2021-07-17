#!/usr/bin/env python
# Automatic Signup, Login, and Post for Wordpress using Selenium Python
# Author: Andrey Ferriyan 
# Script: AutoSignPost.py
# v3.0
#
# Configuration for production use,
# HEADLESS=1, DEBUG=0

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.exceptions import InvalidCredentialsError
import psutil
import time
import platform

class AutoSignPost(object):
    def __init__(self, DEBUG=0, HEADLESS=1, PROXY=None):
        self.PROXY = PROXY
        self.DEBUG = DEBUG
        self.HEADLESS = HEADLESS
        if platform.system() == 'Linux':
            self.FIREFOX_DRIVER="../../aux/firefox/geckodriver"
            self.CHROME_DRIVER="../../aux/chrome/chromedriver"
        elif platform.system() == 'Windows':
            print("You are using Windows OS. Please set your browser driver PATH")

    def _browserDriver(self, browser):
        if self.PROXY is not None:
            if browser == "firefox":
                webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                        'proxyType': "MANUAL",
                        'httpProxy': self.PROXY,
                        'ftpProxy':  self.PROXY,
                        'sslProxy':  self.PROXY,
                        }
            elif browser == "chrome":
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                        'proxyType': "MANUAL",
                        'httpProxy': self.PROXY,
                        'ftpProxy':  self.PROXY,
                        'sslProxy':  self.PROXY,
                        }
        if browser == "firefox":
            browser_opt = webdriver.FirefoxOptions()
            if self.HEADLESS == 1:
                browser_opt.add_argument("--headless")
            if platform.system() == 'Linux':
                bdriver = webdriver.Firefox(executable_path=self.FIREFOX_DRIVER, options=browser_opt)
            else:
                bdriver = webdriver.Firefox(options=browser_opt)
        elif browser == "chrome":
            browser_opt = webdriver.ChromeOptions()
            if self.HEADLESS == 1:
                browser_opt.add_argument("--headless")
            if platform.system() == 'Linux':
                bdriver = webdriver.Chrome(executable_path=self.CHROME_DRIVER, options=browser_opt)
            else:
                bdriver = webdriver.Chrome(options=browser_opt)
        return bdriver

    def signUp(self, urlsignup, user, email, driver):
        """
            signUp
            for random user signup use with LibDGA
        """
        with self._browserDriver(driver) as browser:
            browser.get(urlsignup)
            browser.find_element_by_id("user_login").send_keys(user)
            browser.find_element_by_id("user_email").send_keys(email)
            browser.find_element_by_id("wp-submit").click()
            time.sleep(2)
            browser.quit()
            self._checkDriver(driver)

    def _checkDriver(self, driver):
        """
            check running driver, and close if unused
        """
        for proc in psutil.process_iter():
            if proc.name() == driver:
                proc.kill()

    def _login(self, url, username, password, driver):
        """
            (UNUSED)
            Login
        """
        with self._browserDriver(driver) as browser:
            browser.get("{}/wp-login.php".format(url))
            browser.find_element_by_id("user_login").send_keys(username)
            browser.find_element_by_id("user_pass").send_keys(password)
            browser.find_element_by_id("wp-submit").click()

        return browser

    def loginB(self, url, username, password, driver):
        """
            For BruteForce testing purpose
        """
        loginsuccess = 0 
        with self._browserDriver(driver) as browser: 
            browser.get("{}/wp-login.php".format(url))
            browser.find_element_by_id("user_login").send_keys(username)
            browser.find_element_by_id("user_pass").send_keys(password)
            browser.find_element_by_id("wp-submit").click()

            try:
                print(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#login_error"))).text)
                print("Incorrect Username or Password")
                loginsuccess = 0
            except TimeoutException as e:
                print("Correct username and password")
                loginsuccess = 1
        return loginsuccess 

    def loginX(self, url, username, password, title, content):
        """
        For BruteForce testing purpose with XML-RPC
        """
        success = 0
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = "publish"
        wp = Client(url, username, password)
        try:
            wp.call(NewPost(post))
            success = 1
        except InvalidCredentialsError:
            success = 0
            print("incorrect username or password")

        return success

    def postArticle(self, username, password, driver, urlsrc, urldest=None):
        """
            Login, Post, and Logout
        """
        if urldest == None:
            urldest = "https://vic3.clouds.web.id"

        with self._browserDriver(driver) as browser:
            browser.get("{}".format(urlsrc))
            title_crawl = browser.find_element_by_class_name('entry-title').text
            content_crawl = browser.find_element_by_id('wtr-content').text
        
        #print("pass grabbing title...")
        #print("{}".format(title_crawl))
        
        # still error here
        #browserpost = self._login(urldest, username, password, driver)
        #with self._browserDriver(driver) as browserpost:

            browser.get("{}/wp-login.php".format(urldest))
            browser.find_element_by_id("user_login").send_keys(username)
            browser.find_element_by_id("user_pass").send_keys(password)
            browser.find_element_by_id("wp-submit").click()
            browser.get("{}/wp-admin/post-new.php".format(urldest))
            browser.find_element_by_xpath("//button[@aria-label='Show more tools & options']").click()
            browser.find_element_by_xpath("//button[@aria-label='Code Editor']").click()
            browser.find_element_by_xpath("//*[@id='post-title-1']").send_keys(title_crawl)
            browser.find_element_by_xpath("//*[@id='post-content-0']").send_keys(content_crawl)
            browser.find_element_by_xpath("//button[contains(., 'Publish')]").click()
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".editor-post-publish-button"))).click()        
            
        browser.quit()
        #browserpost.quit()
        self._checkDriver(driver)

    def signIn(self, urlsignin, username, password, driver):
        """
            signin
        """
        with self._browserDriver(driver) as browser:
            browser.get(urlsignin)
            browser.find_element_by_id("user_login").send_keys(username)
            browser.find_element_by_id("user_pass").send_keys(password)
            browser.find_element_by_id("wp-submit").click()
            time.sleep(2)
            browser.quit()
            self._checkDriver(driver)

    def approveUser(self, urlsignin, username, password, driver):
            """
                (UNUSED)
                admin sign and approve user manually and
                generate pass from vulnerable password
            """
            with self._browserDiver(driver) as browser:
                browser.get(urlsignin)
                browser.find_element_by_id("user_login").send_keys(username)
                browser.find_element_by_id("user_pass").send_keys(password)
                browser.find_element_by_id("wp-submit").click()
                time.sleep(2)
                browser.quit()
                self._checkDriver(driver)
