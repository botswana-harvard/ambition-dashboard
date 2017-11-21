from edc_model_wrapper import ModelWrapper

from django.apps import apps as django_apps


class SubjectOffstudyModelWrapper(ModelWrapper):

    model = 'ambition_subject.subjectoffstudy'
    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
    next_url_attrs = ['subject_identifier']
