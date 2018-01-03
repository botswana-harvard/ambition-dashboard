from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'ambition_dashboard'
    admin_site_name = 'ambition_test_admin'
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
