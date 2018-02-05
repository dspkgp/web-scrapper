from scraper import *
import time
import pickle
from pprint import pprint
from pymongo import MongoClient

TOP_LIMIT = 100000

def get_all_data():
	final_list = []
	page = 204

        client = MongoClient("localhost", 8201)
        db = client.careerbuilder

        document_count = 0

	for i in range(204, TOP_LIMIT):
		print "Page number : {}".format(page)

		scrapper = Scrapper(count = i)
		urls = scrapper.get_urls()

		if not urls:
			break

		url_count = 1

		for url in urls:
			print "Url count : {}".format(url_count)

                        resume_scrapper = ResumeScrapper(url)
			company_info = resume_scrapper.get_company_info_data()
			job_title = resume_scrapper.get_job_title()
			job_requirements = resume_scrapper.get_job_requirements()
			job_description_data = resume_scrapper.get_job_description_data()

			document = {
				"url" : url,
				"company_info" : company_info,
				"job_title" : job_title,
				"job_requirements" : job_requirements,
				"job_description_data" : job_description_data
			}

                        db.data.insert(document)
                        document_count = document_count + 1
                        print "Inserted Document {}".format(document_count)

			url_count = url_count + 1

		page = page + 1

        print "Completed the process of scraping careerbuilder, Congratulations!!"
        client.close()

if __name__ == "__main__":
	get_all_data()