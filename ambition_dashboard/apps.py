from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'ambition_dashboard'

    admin_site_name = 'ambition_subject_admin'
    base_template_name = 'edc_base/base.html'
    dashboard_template_name = 'ambition_dashboard/subject/dashboard.html'
    dashboard_url_name = 'ambition_dashboard:dashboard_url'
    listboard_template_name = 'ambition_dashboard/subject/listboard.html'
    listboard_url_name = 'ambition_dashboard:listboard_url'
    screening_listboard_template_name = 'ambition_dashboard/screening/listboard.html'
    screening_listboard_url_name = 'ambition_dashboard:screening_listboard_url'
    include_in_administration_section = False


if settings.APP_NAME == 'ambition_dashboard':

    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='ambition_dashboard.appointment',
                related_visit_model='ambition_dashboard.subjectvisit',
                appt_type='hospital')]
