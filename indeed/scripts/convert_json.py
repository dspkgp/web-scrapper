from pymongo import MongoClient
from test_data import TEST_DATA
from dateutil.parser import parse
import pandas as pd
import numpy as np


def merge_dictionaries(dicts):
    final_dict = {}

    for d in dicts:
        for key, value in d.items():
            final_dict.update({
                    key : value
                })

    return final_dict


def get_latest_work_experience(work_experiences):
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
                        "output_work_date" : work_experiences[i].get('work_date')
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
                "output_work_date" : latest_workex.get('work_date')
            }

    return output_dict


def clean_work_experiences(work_experiences):
    work_experience_key_mapper = {
        "work_title" : "{0}_work_title",
        "work_company" : "{0}_work_company",
        "work_date" : "{0}_work_date"
    }

    if not work_experiences:
        return {}

    workex_dict = {}

    latest_work_experience = get_latest_work_experience(work_experiences)
    remaining_experiences = [workex for workex in work_experiences if workex.get('work_date') != latest_work_experience.get('output_work_date')]

    for i in range(len(remaining_experiences)):
        if i >= 10:
            break

        remaining_experiences[i].pop('work_description')
        for key, value in remaining_experiences[i].items():
            workex_dict.update({
                    work_experience_key_mapper[key].format(i) : value
                })

    final_work_experiences = merge_dictionaries([latest_work_experience, workex_dict])

    return final_work_experiences


def clean_educations(educations):
    education_key_mapper = {
        "education_class" : "{0}_education_class",
        "education_school" : "{0}_education_school",
        "education_title" : "{0}_education_title"
    }

    if not educations:
        return {}

    edu_dict = {}

    for i in range(len(educations)):
        if i >= 10:
            break
        for key, value in educations[i].items():
            edu_dict.update({
                    education_key_mapper[key].format(i) : value
                })

    return edu_dict


def clean_certifications(certifications):
    certification_key_mapper = {
        "certification_title" : "{0}_certification_title",
        "certification_description" : "{0}_certification_description",
        "certification_date" : "{0}_certification_date"
    }

    if not certifications:
        return {}

    cert_dict = {}

    for i in range(len(certifications)):
        if i >= 10:
            break

        for key, value in certifications[i].items():
            cert_dict.update({
                    certification_key_mapper[key].format(i) : value
                })

    return cert_dict


def clean_skills(skills):
    if not skills:
        return {}

    skill_dict = {}

    for i in range(len(skills)):
        skill_dict.update({
                "{0}_skill_name".format(i) : skills[i]
            })

    return skill_dict


def get_cleaned_data(data):
    fields_to_pop = ['_id', 'basic_information', 'additional_information', 'url']
    after_fields_to_pop = ['certifications', 'work_experience', 'educations', 'skills']

    for field in fields_to_pop:
        data.pop(field)

    skills = clean_skills(data.get('skills'))
    certifications = clean_certifications(data.get('certifications'))
    educations = clean_educations(data.get('educations'))
    work_experiences = clean_work_experiences(data.get('work_experience'))

    for field in after_fields_to_pop:
        data.pop(field)

    return merge_dictionaries([skills, certifications, educations, work_experiences, data])


if __name__ == '__main__':
    final_list = []

    # data = get_cleaned_data(TEST_DATA)

    # import ipdb; ipdb.set_trace()

    client = MongoClient("localhost", 8201)
    db = client.indeedml
    counter = 1

    for datum in db.data.find():
        print "Skill : {0}, Counter : {1}".format(datum.get('skill'), counter)

        cleaned_data = get_cleaned_data(datum)

        for key, value in cleaned_data.items():
            if value:
                cleaned_data[key] = value.encode('utf-8')

        final_list.append(cleaned_data)
        counter = counter + 1

    client.close()
    df = pd.DataFrame(final_list)
    df.fillna(value = np.nan, inplace = True)
    df.to_csv("data.csv")
