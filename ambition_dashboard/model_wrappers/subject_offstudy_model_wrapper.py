from django.conf import settings
from edc_model_wrapper import ModelWrapper


class SubjectOffstudyModelWrapper(ModelWrapper):

    model = 'ambition_subject.subjectoffstudy'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
