from django.conf.urls import url
from edc_constants.constants import UUID_PATTERN
from django.conf import settings

from .patterns import subject_identifier, screening_identifier
from .views import ListboardView, DashboardView, ScreeningListboardView


def listboard_urls():
    urlpatterns = []
    listboard_configs = [('listboard_url', ListboardView, 'listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/'
                '(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/',
                listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


def dashboard_urls():
    urlpatterns = []

    dashboard_configs = [('dashboard_url', DashboardView, 'dashboard')]

    for dashboard_url_name, dashboard_view_class, label in dashboard_configs:
        urlpatterns.extend([
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/'
                '(?P<appointment>' + UUID_PATTERN.pattern + ')/',
                dashboard_view_class.as_view(), name=dashboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + UUID_PATTERN.pattern + ')/',
                dashboard_view_class.as_view(), name=dashboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/',
                dashboard_view_class.as_view(), name=dashboard_url_name),
            url(r'^' + label + '/'
                '(?P<subject_identifier>' + subject_identifier + ')/'
                '(?P<schedule_name>' + 'schedule1' + ')/',
                dashboard_view_class.as_view(), name=dashboard_url_name),
        ])
    return urlpatterns


def screening_listboard_urls():
    urlpatterns = []

    listboard_configs = [
        ('screening_listboard_url', ScreeningListboardView, 'screening_listboard')]
    for listboard_url_name, listboard_view_class, label in listboard_configs:
        urlpatterns.extend([
            url(r'^' + label + '/'
                '(?P<screening_identifier>' + screening_identifier + ')/'
                '(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/'
                '(?P<screening_identifier>' + screening_identifier + ')/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/(?P<page>\d+)/',
                listboard_view_class.as_view(), name=listboard_url_name),
            url(r'^' + label + '/',
                listboard_view_class.as_view(), name=listboard_url_name)])
    return urlpatterns


urlpatterns = listboard_urls() + screening_listboard_urls() + dashboard_urls()

if settings.APP_NAME == 'ambition_dashboard':
    from .tests.admin import ambition_subject_admin
    urlpatterns = ([url(r'^admin/', ambition_subject_admin.urls)]
                   + urlpatterns)
