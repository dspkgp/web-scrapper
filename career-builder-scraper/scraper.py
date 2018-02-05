import pickle
import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
from pprint import pprint

class Scrapper(object):

	RESUME_URL = 'http://www.careerbuilder.com/jobs?page_number='

	def __init__(self, count = 1):

		self.DOMAIN = 'http://www.careerbuilder.com'
		self.headers = {
			"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
		}

		self.url = self.RESUME_URL + str(count)

		while True:
			try:
				self.response = requests.get(self.url, headers = self.headers)
			except ConnectionError as exc:
				print repr(exc)
				# time.sleep(10)
				continue
			break


	def get_urls(self):
		urls = []

		response_soup = BeautifulSoup.BeautifulSoup(self.response.content)
		h_element = response_soup.findAll("h2", {"class":"job-title"})
		for element in h_element:
			urls.append(self.DOMAIN + element.find('a').get('href'))

		return urls

class ResumeScrapper(object):

	def __init__(self, url):
		self.url = url

		self.headers = {
			"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
		}

		print "Started parsing at url {}".format(self.url)

		while True:
			try:
				self.response = requests.get(self.url, headers = self.headers)
			except ConnectionError as exc:
				print repr(exc)
				# time.sleep(10)      
				continue

			break

		self.soup = BeautifulSoup.BeautifulSoup(self.response.content)

	def get_company_info_data(self):
		company_info = self.soup.findAll("div", {"class" : "company-info"})

		try:
			company_title = company_info[0].find('header').text
			about_company = company_info[0].find('p').text
		except:
			company_title = None
			about_company = None

		company_info = {
			"company_title" : company_title,
			"about_company" : about_company
			}

		return company_info

	def get_job_title(self):
		job_title_element = self.soup.findAll("h1")

		try:
			job_title = self.soup.findAll("h1")[0].text
		except:
			job_title = None

		return job_title

	def get_job_requirements(self):
		job_posted = self.soup.findAll("div", {"class" : "description"})

		try:
			job_requirements = job_posted[-1].text.split('.')
		except:
			job_requirements = None

		return job_requirements

	def get_job_description(self):
		job_posted = self.soup.findAll("div", {"class" : "description"})

		try:
			job_description = job_posted[0]
		except:
			job_description = None

		return job_description

	def get_data_from_job_description(self, element):
		job_description = self.get_job_description()
		element_list = []
		if job_description:
			html_element = job_description.findAll(element)
			if html_element is not None:
				for elements in html_element:
					element_list.append(elements.text)

		return element_list

	def get_job_description_data(self):
		job_description_data = {}

		div_list = self.get_data_from_job_description('div')
		heading_list = self.get_data_from_job_description('strong')
		paragraph_list = self.get_data_from_job_description('p')
		query_list = self.get_data_from_job_description('li')

		job_description_data.update({
					"div_data" : div_list,
					"headings" : heading_list,
					"paragraph" : paragraph_list,
					"query_data" : query_list
		})

		return job_description_data
