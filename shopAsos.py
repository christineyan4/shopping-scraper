#! /usr/bin/env python3

import webbrowser, sys, requests, bs4, time, random
from selenium import webdriver

class Product:
	def __init__(self, url, price):
		self.url = url
		self.price = price

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
#}

def sorted_insert(item, mins):
	# inserts item into mins, keeping list sorted
	if len(mins) == 0:
		mins.append(item)
	else:
		for i in range(len(mins)):
			if item.price < mins[i].price: 
				mins.insert(i, item)
				return

		if len(mins) < 10:
			mins.append(item)

def find_mins(products, x):
	mins = []
	for i in range(x):
		mins.append(products.pop(min(products)))
	return mins
#########

	# finds x cheapest products in list
	#mins = []

#	for prod in products:

		# if mins isn't full, insert
	#	if len(mins) < x:
	#		sorted_insert(prod, mins)
	#	else:
			# compare with last item in mins (the max)
			#if prod.price < mins[-1].price:
	#		if prod.price < mins[0].price:
	#			sorted_insert(prod, mins)
	#			mins.pop(0)
	#			#mins.pop()

	#return mins

if __name__ == '__main__':
	if len(sys.argv) > 2:
		# need 2 command line args
		# first: number of results to return
		# second: search query

		search = '+'.join(sys.argv[2:])
		pageOne = 'https://us.asos.com/search/?q=' + search

		# new Chrome session
		driver = webdriver.Chrome()
		driver.implicitly_wait(5)
		driver.get(pageOne)

		# Selenium hands page src to Beautiful Soup	
		soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

		results = []
		x = 0

		# scraping data
		for div in soup.find_all('div', {'class': '_3-pEc3l'}):
			for link in div.select('a._3x-5VWa'):

				# go to each link, add Product to list
				driver.get(link['href'])				
				soup2 = bs4.BeautifulSoup(driver.page_source, 'html.parser')
				price = (soup2.find('span', {'itemprop': 'price'})).get_text()
				prod = Product(link['href'], price)
				results.append(prod)
				print(prod.url)
				print(prod.price)

				#go back
				driver.execute_script("window.history.go(-1)") 

		# finding x cheapest items (1st cmd line arg)
		mins = find_mins(results, int(sys.argv[1]))

		# opening links to cheapest x items
		for m in mins:
			webbrowser.open(m.url)

