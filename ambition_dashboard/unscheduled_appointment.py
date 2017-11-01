from django.apps import apps as django_apps
from edc_appointment.appointment_creator import AppointmentCreator
from edc_appointment.constants import NEW_APPT, IN_PROGRESS_APPT
from edc_base.utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


class VisitConfigError(Exception):
    pass


class AppointmentStatusError(Exception):
    pass


class UnscheduledAppointment:

    visit_model = 'ambition_subject.subjectvisit'

    appointment_creator_cls = AppointmentCreator

    def __init__(self, subject_identifier=None, report_datetime=None, **kwargs):

        options = dict(appointment__subject_identifier=subject_identifier)
        if report_datetime:
            options.update(report_datetime__lte=report_datetime)

        visit_obj = self.visit_model_cls.objects.filter(
            **options).order_by('report_datetime').last()

        if visit_obj.appointment.appt_status in [NEW_APPT, IN_PROGRESS_APPT]:
            raise AppointmentStatusError(
                f'Appointment {visit_obj.visit_code} current status is '
                f'{visit_obj.appointment.appt_status}, unscheduled appointment not created.')

        schedule = site_visit_schedules.get_schedule(
            schedule_name=visit_obj.schedule_name)
        visit = schedule.visits.get(visit_obj.visit_code)

        if visit.allow_unscheduled:
            visit_code_sequence = visit_obj.appointment.visit_code_sequence + 1
            appointment_creator = self.appointment_creator_cls(
                model_obj=visit_obj.appointment, visit=visit,
                available_datetime=get_utcnow(),
                timepoint_datetime=get_utcnow(),
                visit_code_sequence=visit_code_sequence
            )
            appointment_creator.update_or_create()
        else:
            raise VisitConfigError(f'Visit {visit_obj.visit_code} is not configured for '
                                   'unscheduled appointment.')

    @property
    def visit_model_cls(self):
        return django_apps.get_model(self.visit_model)
