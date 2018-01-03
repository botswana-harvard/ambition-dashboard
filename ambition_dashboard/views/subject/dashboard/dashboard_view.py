from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_rando.view_mixins import RandomizationListViewMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import CrfModelWrapper, SubjectVisitModelWrapper
from ....model_wrappers import RequisitionModelWrapper, SubjectConsentModelWrapper
from ....model_wrappers import SubjectLocatorModelWrapper


class DashboardView(
        SubjectDashboardViewMixin, RandomizationListViewMixin,
        NavbarViewMixin, EdcBaseViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'ambition_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'consented_subject'
    requisition_model_wrapper_cls = RequisitionModelWrapper
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
