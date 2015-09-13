#! /usr/bin/python

import requests
import re
from bs4 import BeautifulSoup as bs
#from urllib2 import urlopen
import csv

def scrapper(id):
	"""A simple scrapper to scrap details from Bexar County property search.
	This is only a barebone implementation and only done for demonstration purposes.
	I recommend anyone using this to makesure that you don't KILL the server with requests."""

	csv_file = open("bcad_details.csv", 'wt')
	writer = csv.writer(csv_file)
	session_url = "http://www.bcad.org/clientdb/?cid=1"
	url = "http://www.bcad.org/clientdb/Property.aspx?prop_id="+ str(id)
	
	# setting the session, filling the cookie jar
	session = requests.Session()
	sess_page = session.get(session_url) 
 	page = session.post(url) # getting the required info
	parsed_text = bs(page.text, "lxml")
	
	#print parsed_text
	tables = parsed_text.find_all('table')
	#for t in tables:
	#	print t.attrs

	header_row = []
	data_row = []
	csv_row = []
	table_list = parsed_text.find_all('table', {'class': ['tableData']})[2]
	rows = table_list.find_all('tr')
	
	for row in rows:
		for head in row.find_all(['th']):
			header = head.get_text().encode('utf-8')
			header_row.append(header)
	header_row = ['prop_id'] + header_row
	writer.writerow(header_row)
	
	for row in rows:
		for value in row.find_all(['td']):
			data = value.get_text().encode('utf-8')
			data_row.append(data)
			writer.writerow(data_row)


if __name__ == '__main__':
		scrapper() # enter the property-id here as an argument.

