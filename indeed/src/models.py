from mongoengine import *


class BasicInformation(EmbeddedDocument):

    heading = StringField()
    job_title = StringField()
    location = StringField()
    summary = StringField()


class WorkExperience(EmbeddedDocument):

    work_title = StringField()
    work_company = StringField()
    work_date = StringField()
    work_description = StringField()


class Education(EmbeddedDocument):

    education_title = StringField()
    education_school = StringField()
    education_class = StringField()


class Certification(EmbeddedDocument):

    certification_title = StringField()
    certification_date = StringField()
    certification_description = StringField()


class Data(Document):

    url = StringField()
    basic_info = EmbeddedDocumentField(BasicInformation)
    work_experience = EmbeddedDocumentListField(WorkExperience)
    education = EmbeddedDocumentListField(Education)
    skill = ListField()
    certification = EmbeddedDocumentListField(Certification)
    additional_info = StringField()
