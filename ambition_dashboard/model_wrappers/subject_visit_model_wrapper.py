from django.apps import apps as django_apps

from edc_visit_tracking import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper


class SubjectVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'ambition_subject.subjectvisit'
    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
