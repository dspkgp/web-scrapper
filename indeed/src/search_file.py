from elasticsearch import Elasticsearch, RequestsHttpConnection
from settings import ELASTICSEARCH_SETTINGS, MONGO_SETTINGS
from pymongo import MongoClient
from dateutil.parser import parse


def get_latest_work_experience(document_id, work_experiences):
    output_dict = {}
    end_date_to_workex_mapping = {}
    end_dates = []

    for i in range(len(work_experiences)):
        date = work_experiences[i].get('work_date')
        if date:
            if "present" in date.lower():
                output_dict.update({
                        "output_work_title" : work_experiences[i].get('work_title'),
                        "output_work_company" : work_experiences[i].get('work_company'),
                        "output_work_date" : work_experiences[i].get('work_date'),
                        "output_work_description" : work_experiences[i].get('work_description'),
                        "document_id" : str(document_id)
                    })

    if not output_dict:
        for i in range(len(work_experiences)):
            date = work_experiences[i].get('work_date')
            if date:
                split_date = date.split(" to ")
                if len(split_date) == 2:
                    end_dates.append(parse(split_date[1]))
                    end_date_to_workex_mapping.update({
                            parse(split_date[1]) : work_experiences[i]
                        })
        if end_dates:
            max_end_date = max(end_dates)
            latest_workex = end_date_to_workex_mapping[max_end_date]
            output_dict = {
                "output_work_title" : latest_workex.get('work_title'),
                "output_work_company" : latest_workex.get('work_company'),
                "output_work_date" : latest_workex.get('work_date'),
                "output_work_description" : latest_workex.get('work_description'),
                "document_id" : str(document_id)
            }

    return output_dict


def get_single_data_for_bulk(work_experience):
    return {
        "_index" : "jt-index",
        "_type" : "latest-experience",
        "_id" : work_experience.get('document_id'),
        "_source" : work_experience
    }


def main():
    client = MongoClient(MONGO_SETTINGS['HOST'], MONGO_SETTINGS['PORT'])
    db = client.indeedml
    es = Elasticsearch([ELASTICSEARCH_SETTINGS['address']], connection_class=RequestsHttpConnection)
    data = []

    for datum in db.data.find():
        latest_work_experience = get_latest_work_experience(datum.get('_id'), datum.get('work_experience'))

        if not latest_work_experience.get('document_id'):
            continue

        data.append(get_single_data_for_bulk(latest_work_experience))

    res = es.bulk(data)
    print res

    file_name
