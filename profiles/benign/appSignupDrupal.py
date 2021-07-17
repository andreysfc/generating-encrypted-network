#!/usr/bin/env python
# Main Script for automatic sign up and sign in with selenium python
# Author: Andrey Ferriyan 
# Script: appSignupDrupal.py 
# v1.0

from LibDGA import LibDGA as ldga
from AutoSignPost import AutoSignPost as ausi
import logging
import time

URLSIGNUP = "<put your drupal registration link here>"

if __name__ == "__main__":
	NOREG = 100 

	logging.basicConfig(filename="registerdrupal.log", level=logging.DEBUG)
	
	email = ldga()
	aus   = ausi(PROXY="localhost:8080")

	for i in range(NOREG):
	   aus.signUp(URLSIGNUP, email.getRandomEmail(), email.getFirstname(), "firefox")
	   logging.info(URLSIGNUP+","+email.getRandomEmail()+","+email.getFirstname()+",firefox")
	   time.sleep(3)

	for i in range(NOREG):
	   aus.signUp(URLSIGNUP, email.getRandomEmail(), email.getFirstname(), "chrome")
	   logging.info(URLSIGNUP+","+email.getRandomEmail()+","+email.getFirstname()+",chrome")
	   time.sleep(3)
		
