from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_dashboard.model_wrappers import SubjectLocatorModelWrapper
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_appointment.models import Appointment
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.view_mixins import DashboardViewMixin as EdcDashboardViewMixin
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import CrfModelWrapper, SubjectVisitModelWrapper
from ....model_wrappers import RequisitionModelWrapper, SubjectConsentModelWrapper


class DashboardView(
        SubjectDashboardViewMixin, EdcDashboardViewMixin,
        NavbarViewMixin, AppConfigViewMixin, EdcBaseViewMixin,
        TemplateView):

    appointment_model_wrapper_cls = AppointmentModelWrapper
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    subject_locator_model = 'ambition_subject.subjectlocator'

    app_config_name = 'ambition_dashboard'
    consent_model = 'ambition_subject.subjectconsent'
    offstudy_model = 'ambition_subject.subjectoffstudy'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    requisition_model_wrapper_cls = RequisitionModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper

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
            subject_offstudy=self.subject_offstudy,
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
    def subject_offstudy(self):
        model_cls = django_apps.get_model(self.offstudy_model)
        try:
            obj = model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            obj = None
        return obj
