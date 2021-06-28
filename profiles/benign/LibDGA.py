#!/usr/bin/env python
# Random Name Generator for DGA 
# Author: Andrey Ferriyan <andrey@sfc.wide.ad.jp>
# Script: LibDGA.py
# v1.9
# 

import random

class LibDGA(object):
	def __init__(self, properName=None):
		"""
		Initialization
		
		Example:
		>>> from LibDGA import LibDGA as ldga
		>>> email = ldga()	
		"""

		PROPERNAMES="../../raw_data/names/propernames.txt"
		VALIDEMAIL="../../raw_data/emailproviders/valid_email_providers.txt"
		self.properName = properName
		self.fName = None
		self.fMail = None
		if self.properName == None:
			self.fName = PROPERNAMES
			self.fMail = VALIDEMAIL
			print("Using default propernames...")
		else:
			self.fName = self.properName
			self.fMail = self.validEmail
			print("Using custom propernames...")

	def _loadListName(self):
		"""
		Load proper full name list.

		Source: https://svnweb.freebsd.org/csrg/share/dict/propernames?revision=61766&view=co
		"""
		fh = open(self.fName, "r")
		readHandle = fh.readlines()
		fh.close()
		return readHandle	
	
	def _loadValidEmail(self):
		"""
		Load valid email domain list
		Source: https://gist.github.com/tbrianjones/5992856 (updated March 30, 2021)
		"""
		fe = open(self.fMail, "r")
		emailHandle = fe.readlines()
		fe.close()
		return emailHandle

	def _getEmailProvider(self):
		"""
		Get valid email domain
		Example:
		- zonnet.nl
		- hello.hu 
		"""
		emailProv = self._loadValidEmail()
		emailOne = "{}".format(random.choice(emailProv).rstrip("\n"))
		return emailOne

	def getFirstname(self):
		"""
		For user email
		Example: 
		- lucifer
		- Warren
		"""
		first = self._loadListName()
		firstName = "{}".format(random.choice(first).rstrip("\n"))
		return firstName.lower()	

	def randomFullName(self):
		"""
		Get random full name
		
		Example:
		>>> email = ldga()
		>>> email.randomFullName()
		Peggy Devon
		"""
		allName = self._loadListName()	
		firstandlast = "{}".format(random.choice(allName).rstrip("\n")) + " " + "{}".format(random.choice(allName).rstrip("\n"))
		return firstandlast

	def getRandomEmail(self):
		"""
		Get random email address
		
		Example:
		>>> email = ldga()
		>>> email.getRandomEmail()
		warren@zonnet.nl
		
		>>> email.getRandomEmail()
		peggy@happermail.com
		"""
		return "{}".format(self.getFirstname()+"@"+self._getEmailProvider()) 
