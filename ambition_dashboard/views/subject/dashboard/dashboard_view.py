from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_rando.models import RandomizationList
from ambition_screening import EarlyWithdrawalEvaluator
from ambition_visit_schedule import DAY1
from django.apps import apps as django_apps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from edc_appointment.models import Appointment
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import CrfModelWrapper, SubjectVisitModelWrapper
from ....model_wrappers import RequisitionModelWrapper, SubjectConsentModelWrapper
from ....model_wrappers import SubjectLocatorModelWrapper, SubjectOffstudyModelWrapper


class DashboardView(
        SubjectDashboardViewMixin,
        NavbarViewMixin, EdcBaseViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    blood_result_model = 'ambition_subject.bloodresult'
    death_report_model = 'ambition_subject.deathreport'
    study_termination_model = 'ambition_subject.studyterminationconclusion'
    consent_model = 'ambition_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'consented_subject'
    offstudy_model_wrapper_cls = SubjectOffstudyModelWrapper
    requisition_model_wrapper_cls = RequisitionModelWrapper
    subject_locator_model = 'ambition_subject.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    subject_offstudy_model = 'ambition_subject.subjectoffstudy'
    visit_model_wrapper_cls = SubjectVisitModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.check_offstudy_required()
        context.update(
            demographics_listgroup=[
                ('fa-random', self.randomization.short_label)])
        return context

    @property
    def randomization(self):
        """Returns a model instance.
        """
        return RandomizationList.objects.get(
            subject_identifier=self.subject_identifier)

    def empty_appointment(self, **kwargs):
        return Appointment()

    def is_current_enrollment_model(self, enrollment_instance,
                                    schedule=None, **kwargs):
        if (enrollment_instance.schedule_name == 'schedule'):
            return True
        return False

    def check_offstudy_required(self):
        """Offstudy form is required if study_termination or
        death_report exist and the off study form has not
        yet been completed.
        """
        offstudy_required = False
        model_cls = django_apps.get_model(self.subject_offstudy_model)
        try:
            model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            pass
        else:
            for model in [self.study_termination_model, self.death_report_model]:
                model_cls = django_apps.get_model(model)
                try:
                    model_cls.objects.get(
                        subject_identifier=self.subject_identifier)
                except ObjectDoesNotExist:
                    offstudy_required = True
                    break
        return offstudy_required
