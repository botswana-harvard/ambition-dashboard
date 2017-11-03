from django.apps import apps as django_apps
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView
from edc_dashboard.view_mixins import AppConfigViewMixin

from ambition_dashboard.unscheduled_appointment import UnscheduledAppointment
from ambition_dashboard.unscheduled_appointment import VisitConfigError, AppointmentStatusError


class UnscheduledAppointmentView(TemplateView, AppConfigViewMixin):

    template_name = 'ambition_dashboard/subject/dashboard.html'
    app_config_name = 'ambition_dashboard'
    dashboard_url_name = django_apps.get_app_config(
        app_config_name).dashboard_url_name
    unscheduled_app_cls = UnscheduledAppointment

    def get(self, request, *args, **kwargs):
        if kwargs.get('subject_identifier'):
            try:
                self.unscheduled_app_cls(
                    kwargs.get('subject_identifier'))
            except ObjectDoesNotExist as e:
                messages.error(self.request, str(e))
            except VisitConfigError as e:
                messages.warning(self.request, str(e))
            except AppointmentStatusError as e:
                messages.error(self.request, str(e))
        return HttpResponseRedirect(reverse(f'{self.dashboard_url_name}', kwargs=kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'project_name': '{}'.format(
                context.get('project_name'), )
        })
        return context
