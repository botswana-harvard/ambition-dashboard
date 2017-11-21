from django.apps import apps as django_apps
from edc_appointment import AppointmentModelWrapper as BaseAppointmentModelWrapper

from .subject_visit_model_wrapper import SubjectVisitModelWrapper


class AppointmentModelWrapper(BaseAppointmentModelWrapper):

    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
    visit_model_wrapper_cls = SubjectVisitModelWrapper

#     TODO: is this needed?
#     dashboard_url_name = django_apps.get_app_config(
#         'ambition_dashboard').dashboard_url_name
