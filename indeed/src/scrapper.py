import requests
import BeautifulSoup
import logging
from requests.exceptions import ConnectionError
import time


logger = logging.getLogger('indeed')

class Scrapper(object):

    DOMAIN = 'https://www.indeed.com'
    RESUME_URL = DOMAIN + '/resumes/'

    def __init__(self, skill, count = 0):
        self.skill = skill.lower()

        self.headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        }

        self.url = self.RESUME_URL + '?q=' + self.skill + "&start=" + str(count)

        while True:
            try:
                self.response = requests.get(self.url, headers = self.headers)
            except ConnectionError as exc:
                logger.info("Following error occured : {0}".format(repr(exc)))
                time.sleep(20)
                continue

            break


    def preprocess(self):
        if not self.response.status_code == 200:
            logger.error("Following status code was raised : {0}".format(self.response.status_code))
            return {}

        response_soup = BeautifulSoup.BeautifulSoup(self.response.content)
        ol_html = response_soup.find("ol", {"id" : "results"})
        li_tags = ol_html.findAll('li')
        total_li_elements = len(li_tags)
        title_to_href_mapping = {}

        for i in range(0, total_li_elements):
            a_element = li_tags[i].find("a", {"class" : "app_link"})
            title_to_href_mapping.update({a_element.text : a_element.get('href')})

        return title_to_href_mapping


class ResumeScrapper(object):

    DOMAIN = 'https://www.indeed.com'

    def __init__(self, url, *args, **kwargs):
        self.url = self.DOMAIN + url
        self.title = kwargs.get('title')

        self.headers = {
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        }

        logger.info("Started parsing for {0} at url {1}".format(self.title, self.url))

        while True:
            try:
                self.response = requests.get(self.url, headers = self.headers)
            except ConnectionError as exc:
                logger.info("Following error occured : {0}".format(repr(exc)))
                time.sleep(20)      
                continue

            break

        self.soup = BeautifulSoup.BeautifulSoup(self.response.content)

    def get_text_safely(self, element):
        if not element:
            return None

        return element.text.encode('utf-8')

    def preprocess(self):
        basic_info = self.get_basic_info_content()
        workexperiences = self.get_workexperience_content()
        educations = self.get_education_content()
        skills = self.get_skill_content()
        certifications = self.get_certification_content()
        additional_info = self.get_additional_information_content()

        return basic_info, workexperiences, educations, skills, certifications, additional_info

    def get_basic_info_content(self):
        basic_info_html = self.soup.find("div", {"class" : "last basicInfo-content"})

        if not basic_info_html:
            return {
                "heading" : None,
                "job_title" : None,
                "location" : None,
                "summary" : None
            }

        heading = self.get_text_safely(basic_info_html.find("h1", {"id" : "resume-contact"}))
        job_title = self.get_text_safely(basic_info_html.find("h2", {"id" : "headline"}))
        location = self.get_text_safely(basic_info_html.find("p", {"id" : "headline_location"}))
        summary = self.get_text_safely(basic_info_html.find("p", {"id" : "res_summary"}))

        return {
            "heading" : heading,
            "job_title" : job_title,
            "location" : location,
            "summary" : summary
        }

    def get_workexperience_content(self):
        workex_html = self.soup.find("div", {"class" : "section-item workExperience-content"})

        if not workex_html:
            return []

        workex_divs = workex_html.findAll("div", {"id" : lambda x: x and "workExperience-" in x})

        work_experiences = []

        for workex_div in workex_divs:
            try:
                work_title = self.get_text_safely(workex_div.find("p", {"class" : "work_title title"}))
                work_company = self.get_text_safely(workex_div.find("div", {"class" : "work_company"}).find("span", {"class" : "bold"}))
                work_date = self.get_text_safely(workex_div.find("p", {"class" : "work_dates"}))
                work_description = self.get_text_safely(workex_div.find("p", {"class" : "work_description"}))

                work_experiences.append({
                        "work_title" : work_title,
                        "work_company" : work_company,
                        "work_date" : work_date,
                        "work_description" : work_description
                    })
            except Exception as exc:
                logger.info("Following exception was raised : {0}".format(repr(exc)))

        return work_experiences

    def get_education_content(self):
        education_html = self.soup.find("div", {"class" : "section-item education-content"})

        if not education_html:
            return []

        education_divs = education_html.findAll("div", {"id" : lambda x: x and "education-" in x})

        educations = []

        for education_div in education_divs:
            education_title = self.get_text_safely(education_div.find("p", {"class" : "edu_title"}))
            education_school = self.get_text_safely(education_div.find("div", {"class" : "edu_school"}).find("span", {"class" : "bold"}))
            education_class = self.get_text_safely(education_div.find("p", {"class" : "edu_dates"}))

            educations.append({
                    "education_title" : education_title,
                    "education_school" : education_school,
                    "education_class" : education_class
                })

        return educations

    def get_skill_content(self):
        skill_html = self.soup.find("div", {"class" : "section-item skills-content"})

        if not skill_html:
            return []

        if skill_html.find("div", {"class" : "skill-container resume-element"}).find("span", {"class" : "skill-text"}):
            return skill_html.find("div", {"class" : "skill-container resume-element"}).find("span", {"class" : "skill-text"}).text.split(",")

        return []

    def get_certification_content(self):
        certification_html = self.soup.find("div", {"class" : "section-item certification-content"})

        if not certification_html:
            return []

        certification_divs = certification_html.findAll("div", {"id" : lambda x: x and "certification-" in x})
        certifications = []

        for certification_div in certification_divs:
            certification_title = self.get_text_safely(certification_div.find("p", {"class" : "certification_title"}))
            certification_date = self.get_text_safely(certification_div.find("p", {"class" : "certification_date"}))
            certification_description = self.get_text_safely(certification_div.find("p", {"class" : "certification_description"}))

            certifications.append({
                    "certification_title" : certification_title,
                    "certification_date" : certification_date,
                    "certification_description" : certification_description
                })

        return certifications

    def get_additional_information_content(self):
        additional_information_html = self.soup.find("div", {"class" : "section-item additionalInfo-content"})

        if not additional_information_html:
            return ""

        return self.get_text_safely(additional_information_html.find("div", {"id" : "additionalinfo-section"}))
