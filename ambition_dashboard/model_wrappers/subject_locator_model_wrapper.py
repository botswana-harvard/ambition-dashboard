from django.apps import apps as django_apps
from edc_model_wrapper.wrappers import ModelWrapper


class SubjectLocatorModelWrapper(ModelWrapper):

    model = 'ambition_subject.subjectlocator'
    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
    next_url_attrs = ['subject_identifier']
