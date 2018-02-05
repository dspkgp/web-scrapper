from settings import app, MONGO_SETTINGS
# from models import *
from scrapper import *
from pymongo import MongoClient
import logging


logger = logging.getLogger("indeed")


@app.task
def parse_resume(url, title, skill):
    logger.info("~~~~~~~~~~~~~~Celery Task set for title : {0} at url : {1}~~~~~~~~~~~~~".format(title, url))
    client = MongoClient(MONGO_SETTINGS.get('HOST'), MONGO_SETTINGS.get('port'))
    db = client.indeedml

    parse = ResumeScrapper(url, title = title)
    basic_info, workexperiences, educations, skills, certifications, additional_info = parse.preprocess()

    print "#########################################################################"
    print skill, basic_info, educations, skills, certifications
    print "#########################################################################"

    db.title_description.insert({
        # "skill" : skill,
        "title" : skill,
        "url" : url,
        "basic_information" : basic_info,
        "work_experience" : workexperiences,
        "educations" : educations,
        "skills" : skills,
        "certifications" : certifications,
        "additional_information" : additional_info
    })

    client.close()
    logger.info("~~~~~~~~~~~~~~~~~~Created entry for resume at url: {0} and title: {1}~~~~~~~~~~~~~~~~~~~~~".format(parse.url, title))
