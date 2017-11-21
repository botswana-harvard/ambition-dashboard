from edc_appointment.models import Appointment
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.view_mixins import DashboardViewMixin as EdcDashboardViewMixin

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from ambition_dashboard.model_wrappers import (
    SubjectLocatorModelWrapper, SubjectOffstudyModelWrapper)
from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_subject.eligibility import EarlyWithdrawalEvaluator
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import CrfModelWrapper, SubjectVisitModelWrapper, SubjectConsentModelWrapper
from ....model_wrappers import RequisitionModelWrapper


class DashboardView(
        SubjectDashboardViewMixin, EdcDashboardViewMixin,
        NavbarViewMixin, AppConfigViewMixin, EdcBaseViewMixin,
        TemplateView):

    appointment_model_wrapper_cls = AppointmentModelWrapper
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    subject_locator_model = 'ambition_subject.subjectlocator'

    app_config_name = 'ambition_dashboard'
    consent_model = 'ambition_subject.subjectconsent'
    subject_offstudy_model = 'ambition_subject.subjectoffstudy'
    blood_result_model = 'ambition_subject.bloodresult'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    offstudy_model_wrapper_cls = SubjectOffstudyModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
    requisition_model_wrapper_cls = RequisitionModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'consented_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_url_name = django_apps.get_app_config(
            self.app_config_name).dashboard_url_name
        context.update(
            offstudy_required=self.offstudy_required,
            dashboard_url_name=dashboard_url_name)
        return context

    def empty_appointment(self, **kwargs):
        return Appointment()

    def is_current_enrollment_model(self, enrollment_instance,
                                    schedule=None, **kwargs):
        if (enrollment_instance.schedule_name == 'schedule'):
            return True
        return False

    @property
    def blood_result_model_cls(self):
        try:
            model_cls = django_apps.get_model(self.blood_result_model)
        except LookupError as e:
            raise Exception(
                f'Unable to lookup subject blood result model. '
                f'model={self.blood_result_model}. Got {e}')
        return model_cls

    def offstudy_required(self):
        try:
            model_cls = self.blood_result_model_cls
            blood_result = model_cls.objects.get(
                subject_visit__subject_identifier=self.subject_identifier,
                subject_visit__visit_code='1000')
        except model_cls.DoesNotExist:
            return False
        else:
            obj = EarlyWithdrawalEvaluator(
                alt=blood_result.alt,
                pmn=blood_result.absolute_neutrophil,
                platlets=blood_result.platelets)
            return not obj.eligible
