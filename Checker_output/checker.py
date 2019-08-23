#/usr/bin/python3
import os
import requests
from os import path
import re

class Checkers:
	#def __init__(self):

	def OutputCheck(self,var_in):
		switcher = {
			0: "\033[1;32;40m GOOD \033[0m",
			1: "\033[1;37;40m UNKNOWN \033[0m",
			2: "\033[1;31;40m BAD \033[0m",
			3: "\033[1;33;40m WARNING \033[0m"}
		return(switcher.get(var_in, "Invalid input"))

	def OsCheck(self):
		if path.exists("/etc/debian_version") == True:
				self.Distrib = "Debian-based"
				comment = "It\'s all good"
				Conf_default_path = "/etc/apache2/apache2.conf"
				Siteen_default_path = "/etc/apache2/sites-enabled/"
				Modsen_default_path = "/etc/apache2/mods-enabled/"
				status=0
		elif path.exists("/etc/redhat-release") == True:
				self.Distrib = "Redhat-based"
				comment = "It\'s all good"
				status=0
		elif path.exists("/etc/fedora-release") == True:
				self.Distrib = "Redhat-based"
				comment = "It\'s all good"
				status=0
		else:
				comment="You\'re using unsupported Distrib"
				status=2
		out = self.OutputCheck(status)
		return(["Linux Distrib",self.Distrib,comment,out])
	
	def VersionCheck(self):
		if self.Distrib == "Debian-based":
			a2currentversion = os.popen('apache2ctl -V |grep "Server version:" |cut -d \"/\" -f2|cut -d \" \" -f1 ').readline().rstrip()
			resp = requests.get("https://httpd.apache.org/download.cgi",stream=True)
			for line in resp.iter_lines():
				if re.search("#apache24",str(line)):
					if re.search("released",str(line)):
						a2latestversion=line
						break
			a2latestversion = re.search('<a href="#apache24">(.*)</a>',str(a2latestversion))
			a2latestversion = a2latestversion.group(1)
			a2latest_maj,a2latest_majsub,a2latest_minor =a2latestversion.split(".")
			a2current_maj,a2current_majsub,a2current_minor =a2currentversion.split(".")
			if (a2current_maj+a2current_majsub) == (a2latest_maj+a2latest_majsub):
				if a2current_minor < a2latest_minor:
					comment="Your version is not the latest"
					status=2
				elif a2current_minor > a2latest_minor:
					comment="Your version is in the future minor release"
					status=3
				else: 
					comment = "You\'re up to date ! "
					status=0
			elif (a2current_maj+a2current_majsub) < (a2latest_maj+a2latest_majsub):
				status=2
				comment = "Your version is not the lastest major release ! "
			elif (a2current_maj+a2current_majsub) > (a2latest_maj+a2latest_majsub):
				status=2
				comment = "Your version is in future ! "
		return(["Apache2 version",a2currentversion, comment, self.OutputCheck(status)])


	def SiteSimpleCheck(self):
		if self.Distrib == "Debian-based":
			a2currentsite = os.popen('a2query -s').readline().rstrip()
			i=0
			comment=""
			status=""
			result=[]
			for line in a2currentsite.split(os.linesep):
				i=i+1
				if re.search("000-default",str(line)):
					comment = "It seems that default site is running."
					status = 2
			result=["Number of sites running",i, comment, self.OutputCheck(status)]
			return(result)

	def ModsSimpleCheck(self):
		if self.Distrib == "Debian-based":
			a2currentmods = os.popen('a2query -m').read().rstrip()
			i=0
			comment=""
			status=0
			result=[]
			for line in a2currentmods.split(os.linesep):
				i=i+1
			result+=["Number of mods running",i, comment, self.OutputCheck(status)]
			return(result)

	def SSLCheck(self):
		if self.Distrib == "Debian-based":
			a2currentmods = os.popen('a2query -m').read().rstrip()
			comment=""
			i=0
			status=0
			for line in a2currentmods.split(os.linesep):
				if re.search("ssl",str(line)):
					comment = "It seems you\'re' using SSL. Well played!"
					status = 0
					break
				else:
					comment = "It seems you\'re' NOT using SSL. Everything is humad readeable on the network..."
					status = 2
			result=["SSL is running ? ",line, comment, self.OutputCheck(status)]
			return(result)
	def EvasiveCheck(self):
		if self.Distrib == "Debian-based":
			a2currentmods = os.popen('a2query -m').read().rstrip()
			comment=""
			i=0
			status=0
			for line in a2currentmods.split(os.linesep):
				if re.search("evasive",str(line)):
					comment = "It seems you\'re using Evasive Mod!"
					status = 0
					break
				else:
					comment = "It seems you\'re' NOT using ModEvasive. You love DOS attack ? "
					status = 2
			result=["ModEvasive is running ? ",line, comment, self.OutputCheck(status)]
			return(result)
	def SecurityCheck(self):
		if self.Distrib == "Debian-based":
			a2currentmods = os.popen('a2query -m').read().rstrip()
			comment=""
			i=0
			status=0
			for line in a2currentmods.split(os.linesep):
				if re.search("security",str(line)):
					comment = "It seems you\'re using Security Mod!"
					status = 0
					break
				else:
					comment = "It seems you\'re' NOT using ModSecurity. You love DOS attack ? "
					status = 2
			result=["ModSecurity is running ? ",line, comment, self.OutputCheck(status)]
			return(result)