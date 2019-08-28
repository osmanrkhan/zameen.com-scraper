#program to scrape zameen.com for Lampro Mellon by Osman Rahim Khan. Date: Aug 22, 2019


from selenium import webdriver
from bs4 import BeautifulSoup
import ssl
from urllib.request import Request, urlopen
import re
from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv 
import numpy as np


class PlotScraper:
	#webdriver automates chrome to access the course page

	#initialize lists
	def __init__(self, link):
		self.link = link
		self.ID = []
		self.LOCATION = []
		self.CITY = []
		self.PRICE = []
		self.STYLE = []
		self.OWNER = []
		self.TYPE = []
		self.PLOT_SIZE = []
		self.PLOT_PRICE = []
		self.PAYMENT_PLAN = []
		self.WEBLINK = []


	#clicks city and house options
	def select_options(self, next_number = 0):

		#select Karachi
		city_dropdown = driver.find_elements_by_xpath\
		('//*[@id="submit_advance_search_np_search"]/div[1]/div/div[1]/div[1]')
		city_dropdown[0].click()

		city = driver.find_elements_by_xpath\
		('//*[@id="city"]/li[2]')
		city[0].click()


		#select houses
		plot_dropdown = driver.find_elements_by_xpath\
		('//*[@id="submit_advance_search_np_search"]\
			/div[1]/div/div[1]/div[3]')
		plot_dropdown[0].click()

		plot_type = driver.find_elements_by_xpath\
		('//*[@id="submit_advance_search_np_search"]\
			/div[1]/div/div[1]/div[3]/div[2]/ul[1]/li[2]')
		plot_type[0].click()

		plot = driver.find_elements_by_xpath\
		('//*[@id="submit_advance_search_np_search"]\
			/div[1]/div/div[1]/div[3]/div[2]/ul[2]/li[1]')
		plot[0].click()

		#hit submit
		submit = driver.find_element_by_id('npSubmit')
		submit.click()

		#go to appropriate page on every restart after a page is parsed
		if (next_number != 0):
			xpath_num = next_number + 2

			page_btn_xpath = \

			'//*[@id="pagination_listing"]/ul/li[' + str(xpath_num) + ']'

			next_page = driver.find_elements_by_xpath(page_btn_xpath)
			next_page[0].click()



	#opens zameen.com page first time
	def open_page(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument("--test-type")
		options.binary_location = "/usr/bin/chromium"
		options.add_experimental_option("detach", True)
		global driver
		driver = webdriver.Chrome\
		('//Users/osmankhan/Desktop/dartmouth_year_2/Scraper/chromedriver')

		driver.get(self.link)
		self.select_options()





	def search_parser(self, next_number = 0):
		#Goes through all properties, runs page parser on each

		#creates thr soup and finds link containers and links in them
		soup = BeautifulSoup(driver.page_source, features="html.parser")
		link_area = soup.find('ul', {'id' : 'np_search_listing_section'})
		links = [a['href'] for a in link_area.find_all('a', href=True)]

		#runs page parser on each link on the search page
		for link in links:
			self.page_parser(link)


		#loads to dataframe
		df = pd.DataFrame(columns = ['ID'])
		df['ID'] = self.ID
		df['Location']= self.LOCATION
		df['Price Range']= self.PRICE
		df['City']= self.CITY
		df['House Style']= self.STYLE
		df['Owner']= self.OWNER
		df['Plot Types'] = self.TYPE
		df['Plot Sizes'] = self.PLOT_SIZE
		df['Plot Prices']= self.PLOT_PRICE
		df['Link to Payment Plan'] = self.PAYMENT_PLAN
		df['Webpage'] = self.WEBLINK

		#prints to excel file
		df.to_csv('/Users/osmankhan/desktop/zameen_karachi_data_payment.csv')



		#iterates next_num, goes to next page at the end of each full search
		xpath_num = next_number + 2
		page_btn_xpath = '//*[@id="pagination_listing"]/ul/li[' + str(xpath_num) + ']'
		next_page = driver.find_elements_by_xpath(page_btn_xpath)
		next_page[0].click()
		next_num = next_number + 1
		if (next_num < 2):
			self.search_parser(next_num)
		


	def page_parser(self, link):
		#sets up arrays that store data before pushing to .csv file
		req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
		page = urlopen(req).read()
		soup = BeautifulSoup(page, features="html.parser")
		data_list = [0] * 6

		#only parses the general data table
		to_search = soup.find('section', {'id' : 'overview'})

		values_needed = to_search.find_all('div', {'class' : 'value left'})
		i = 0

		#goes through each value in the general data
		for row in values_needed:

			data_list[i] = (((((str(row).strip('<div class="value left">'))\
				.strip("</div>")).replace("<span>", "")).replace("\t", ""))\
				.replace("\n", "")).replace("</span>", "")
			i += 1


		self.ID.append(data_list[0])
		self.CITY.append(data_list[1])
		self.LOCATION.append(data_list[2])
		self.PRICE.append(data_list[3])
		self.STYLE.append(data_list[4])
		self.OWNER.append(data_list[5])


		self.update_lists(soup, link)




	def update_lists(self, soup, link):
		#this will get the small plot sizes and prices 
		find_plot_headers = soup.find('div', {'id' : 'propertytypes'})

		find_types = find_plot_headers.find_all('div', {'class' : 'category'})

		#gets property types
		i = 0
		type_data_list = [0] * len(find_types)
		for row1 in find_types:
			stripped_row1 = ((((str(row1).strip('<div class="category">'))\
				.strip("</div>")).replace("\t", "")).replace("\n", ""))\
				.replace(" ", "").replace("</span>", "").replace("<span>", "")

			if (stripped_row1 != "0" and not str.isdigit(stripped_row1)):
				type_data_list[i] = stripped_row1
				i += 1

		#appends types
		x = 0
		type_entry = ""
		while x < len(type_data_list):
			type_entry = type_entry + str(type_data_list[x]) + "\n"
			x += 1

		self.TYPE.append(type_entry)


		find_values = find_plot_headers.find_all('span', {'class' : 'value left'})


		i = 0
		specific_data_list = [0] * len(find_values)

		#gets plot sizes and price
		for row in find_values:

			stripped_row = (((((str(row).strip('<span class="value left">'))\
				.strip("</div>")).replace("\t", ""))\
				.replace("\n", "")).replace("</span>", "")).replace("<span>", "").replace(" ", "")

			if (stripped_row != "0" and not str.isdigit(stripped_row)):
				specific_data_list[i] = stripped_row
				i += 1


		#appends plots
		plot_entry = ""
		a = 0
		while a < len(specific_data_list):
			plot_entry = plot_entry + str(specific_data_list[a]) + "\n"
			a += 2
		self.PLOT_SIZE.append(plot_entry)

		

		#append price entries
		price_entry = ""
		a = 1
		while a < len(specific_data_list):
			price_entry = price_entry + str(specific_data_list[a]) + "\n"
			a += 2

		self.PLOT_PRICE.append(price_entry)


		#get payment plan entries


		link_area = soup.find('section', {'id' : 'paymentplan'})
		link_entry = ""
		if (link_area != None): 

			specific_data_list = [0] * len(link_area.find_all('li'))
			
			for img in link_area.find_all('li'):
				link_entry = link_entry + str(img.get('data-src')) + "\n"

		self.PAYMENT_PLAN.append(link_entry)
		self.WEBLINK.append(link)