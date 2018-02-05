from scraper import *
import time
import pickle
from pprint import pprint
from pymongo import MongoClient

TOP_LIMIT = 100000
def get_all_data():
    final_list = []
    page = 5

    client = MongoClient("localhost", 8201)
    db = client.monster

    document_count = 0

    for i in range(5, TOP_LIMIT):
        print "Page number : {}".format(page)

        scrapper = Scrapper(count = i)
        urls = scrapper.get_urls()

        if not urls:
            break

        url_count = 1

        for url in urls:
            print "Url count : {}".format(url_count)

            resume_scrapper = ResumeScrapper(url)
            about_company = resume_scrapper.get_company_info_data()
            job_title = resume_scrapper.get_job_title()
            job_skills = resume_scrapper.get_job_skills()
            job_description = resume_scrapper.get_job_description()
            summary = resume_scrapper.get_summary_data()

            document = {
                "url" : url,
                "company_info" : about_company,
                "job_title" : job_title,
                "job_skills" : job_skills,
                "job_description" : job_description,
                "sumamry" : summary 
            }

            db.data.insert(document)
            document_count = document_count + 1
            print "Inserted Document {}".format(document_count)         

            url_count = url_count + 1

        page = page + 1

    print "Completed the process of scraping monster, Congratulations!!"
    client.close()

if __name__ == "__main__":
    get_all_data()