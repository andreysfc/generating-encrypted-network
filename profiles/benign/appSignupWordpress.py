#!/usr/bin/env python
# Main Script for automatic sign up and sign in with selenium python
# Author: Andrey Ferriyan <andrey@sfc.wide.ad.jp>
# Script: app.py
# v1.0

from LibDGA import LibDGA as ldga
from AutoSignPost import AutoSignPost as ausi
import logging
import time

URLSIGNUP="<put your wordpress sign up url here>"

if __name__ == "__main__":
	NOREG = 100 

	logging.basicConfig(filename="registration.log", level=logging.DEBUG)
	
	email = ldga()
	aus   = ausi(PROXY="localhost:8080")

	for i in range(NOREG):
	   aus.signUp(URLSIGNUP, email.getFirstname(), email.getRandomEmail(), "firefox")
	   logging.info(URLSIGNUP+","+email.getFirstname()+","+email.getRandomEmail()+",firefox")
	   time.sleep(3)

	for i in range(NOREG):
	   aus.signUp(URLSIGNUP, email.getFirstname(), email.getRandomEmail(), "chrome")
	   logging.info(URLSIGNUP+","+email.getFirstname()+","+email.getRandomEmail()+",chrome")
	   time.sleep(3)
		
