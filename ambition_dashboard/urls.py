from django.conf import settings
from django.urls.conf import path, re_path, include
from edc_constants.constants import UUID_PATTERN

from .patterns import subject_identifier, screening_identifier
from .views import SubjectListboardView, SubjectDashboardView, ScreeningListboardView
from .views import UnscheduledAppointmentView

app_name = 'ambition_dashboard'


def listboard_urls():
    urlpatterns = []
    listboard_configs = [('listboard_url', SubjectListboardView, 'listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/'
                    '(?P<page>\d+)/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/(?P<page>\d+)/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/',
                    listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


def dashboard_urls():
    urlpatterns = []

    dashboard_configs = [('dashboard_url', SubjectDashboardView, 'dashboard')]

    for dashboard_url_name, dashboard_view_class, label in dashboard_configs:
        urlpatterns.extend([
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/'
                    '(?P<appointment>' + UUID_PATTERN.pattern + ')/',
                    dashboard_view_class.as_view(), name=dashboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/',
                    dashboard_view_class.as_view(), name=dashboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/',
                    dashboard_view_class.as_view(), name=dashboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<subject_identifier>' + subject_identifier + ')/'
                    '(?P<schedule_name>' + 'schedule' + ')/',
                    dashboard_view_class.as_view(), name=dashboard_url_name),
        ])
    return urlpatterns


def screening_listboard_urls():
    urlpatterns = []

    listboard_configs = [
        ('screening_listboard_url', ScreeningListboardView, 'screening_listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            re_path(r'^' + label + '/'
                    '(?P<screening_identifier>' + screening_identifier + ')/'
                    '(?P<page>\d+)/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/'
                    '(?P<screening_identifier>' + screening_identifier + ')/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/(?P<page>\d+)/',
                    listboard_view_class.as_view(), name=listboard_url_name),
            re_path(r'^' + label + '/',
                    listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


urlpatterns = listboard_urls() + screening_listboard_urls() + dashboard_urls() + [
    re_path(r'^unscheduled_appointment/(?P<subject_identifier>' + subject_identifier + ')/$',
            UnscheduledAppointmentView.as_view(), name='unscheduled_appointment_url'), ]

if settings.APP_NAME == 'ambition_dashboard':

    from django.views.generic.base import RedirectView
    from edc_base.views import LoginView, LogoutView

    from .tests.admin import ambition_subject_admin

    urlpatterns += [
        path('edc_device/', include('edc_device.urls')),
        path('edc_protocol/', include('edc_protocol.urls')),
        path(r'^admin/', ambition_subject_admin.urls),
        path('admininistration/', RedirectView.as_view(url='admin/'),
             name='administration_url'),
        path('login', LoginView.as_view(), name='login_url'),
        path('logout', LogoutView.as_view(
            pattern_name='login_url'), name='logout_url'),
        path(r'', RedirectView.as_view(url='admin/'), name='home_url')]
