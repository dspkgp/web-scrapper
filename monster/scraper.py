import pickle
import logging
import BeautifulSoup
import requests
from requests.exceptions import ConnectionError

class Scrapper(object):

	RESUME_URL = 'http://jobsearch.monsterindia.com/searchresult-'

	def __init__(self, count = 1):

		self.payload = "fts=&lmy=&ind=65&ctp=0&job="
		self.headers = {
			 "Content-Type" : "application/x-www-form-urlencoded"
		}

		self.url = self.RESUME_URL + str(count) + '.html'

		while True:
			try:
				self.response = requests.get(self.url, headers = self.headers, data = self.payload)
			except ConnectionError as exc:
				print(repr(exc))
				# time.sleep(10)
				continue

			break

	def get_urls(self):
		urls = []

		response_soup = BeautifulSoup.BeautifulSoup(self.response.content)
		hyperlinks = response_soup.findAll("a", {"class":"title_in"})
		for links in hyperlinks:
			urls.append(str(links.get('href')))

		return urls

class ResumeScrapper(object):

	def __init__(self, url):

		self.url = url

		self.headers = {
			"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
		}

		while True:
			try:
				self.response = requests.get(self.url, headers = self.headers)
			except ConnectionError as exc:
				print(repr(exc))
				# time.sleep(10)
				continue

			break

		self.soup = BeautifulSoup.BeautifulSoup(self.response.content)

	def get_company_info_data(self):
		about_company_data = self.soup.findAll("div", {"class" : "desc"})

		try:
			about_company = about_company_data[-1].text.strip()
		except:
			about_company = None

		return about_company

	def get_job_title(self):
		job_title_element = self.soup.findAll("div", {"class" : "job_title"})

		try:
			job_title = job_title_element[0].text
		except:
			job_title = None

		return job_title

	def get_job_description(self):
		job_posted = self.soup.findAll("div", {"class" : "desc"})

		try:
			job_description = job_posted[0].text.strip()
		except:
			job_description = None

		return job_description

	def get_job_skills(self):
		job_skills_element = self.soup.findAll("div", {"class" : "keyskill"})

		try:
			job_skills = job_skills_element[0].text.split(':')[-1]
		except:
			job_skills = None

		return job_skills

	def get_summary_data(self):
		summary_data = self.soup.findAll("div", {"class" : "col-md-3 col-xs-12 pull-right jd_rol_section"})
		try:
			heading_data = summary_data[0].findAll("div", {"class" : "heading"})
			span_data = summary_data[0].findAll('span')

			summary = {}
			for heading,i in zip(heading_data, range(len(span_data))):
				try:
					summary.update({heading.text : (span_data[i].findAll('a')[0].get('title'))})
				except:
					continue
		except:
			summary = {}
		return summary
