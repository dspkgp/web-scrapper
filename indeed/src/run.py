from scrapper import Scrapper
from settings import LOGGING
from tasks import parse_resume
import logging.config
import time
import random
from itertools import islice


logging.config.dictConfig(LOGGING)

logger = logging.getLogger("indeed")

DELAY_VALUES = [3, 4, 5]
# NEXT_COUNT_VALUES = [i for i in range(30, 50)]
NEXT_COUNT_VALUES = [i for i in range(20, 30)]
# NEXT_COUNT_VALUES = [1,2,3,4,5,6]

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


if __name__ == '__main__':
    f = open("data/jts.txt", 'r')

    for title in f:
        logger.info("Title Value: {0}, Count : {1}".format(title, 0))
        scrapper = Scrapper(skill = title, count = 0)
        title_to_href_mapping = scrapper.preprocess()

        n_items = take(2, title_to_href_mapping.iteritems())

        for element in n_items:
            parse_resume.delay(element[1], element[0], title)
            time.sleep(1)

        time.sleep(random.choice(NEXT_COUNT_VALUES))


    # for skill in f:
    #     for count in range(0,200,50):
    #         logger.info("Skill Value: {0}, Count : {1}".format(title, 0))

    #         scrapper = Scrapper(skill = skill, count = 0)
    #         title_to_href_mapping = scrapper.preprocess()

    #         if not title_to_href_mapping:
    #             break



    #         for key, value in title_to_href_mapping.items():
    #             parse_resume.delay(value, key, skill)
    #             time.sleep(random.choice(DELAY_VALUES))

    #     time.sleep(random.choice(NEXT_COUNT_VALUES))

    f.close()
