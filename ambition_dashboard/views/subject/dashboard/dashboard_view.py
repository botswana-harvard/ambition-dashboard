from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.view_mixins import DashboardViewMixin as EdcDashboardViewMixin

from ....model_wrappers import CrfModelWrapper, SubjectVisitModelWrapper
from ....model_wrappers import RequisitionModelWrapper, SubjectConsentModelWrapper
from .base_dashboard_view import BaseDashboardView


class DashboardView(
        BaseDashboardView, EdcDashboardViewMixin,
        AppConfigViewMixin, EdcBaseViewMixin,
        TemplateView):

    app_config_name = 'ambition_dashboard'
    consent_model = 'ambition_subject.subjectconsent'
    offstudy_model = 'ambition_subject.subjectoffstudy'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    crf_model_wrapper_cls = CrfModelWrapper
    requisition_model_wrapper_cls = RequisitionModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper

    navbar_item_selected = 'ambition_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_url_name = django_apps.get_app_config(
            'ambition_dashboard').dashboard_url_name
        context.update(
            subject_offstudy=self.subject_offstudy,
            dashboard_url_name=dashboard_url_name)
        return context

    @property
    def subject_offstudy(self):
        model_cls = django_apps.get_model(self.offstudy_model)
        try:
            obj = model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            obj = None
        return obj
