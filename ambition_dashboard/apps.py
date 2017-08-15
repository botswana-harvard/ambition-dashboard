from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'ambition_dashboard'

    admin_site_name = 'ambition_subject_admin'
    base_template_name = 'edc_base/base.html'
    dashboard_template_name = 'ambition_dashboard/subject/dashboard.html'
    dashboard_url_name = 'ambition_dashboard:dashboard_url'
    listboard_template_name = 'ambition_dashboard/subject/listboard.html'
    listboard_url_name = 'ambition_dashboard:listboard_url'
    screening_listboard_template_name = 'ambition_dashboard/screening/listboard.html'
    screening_listboard_url_name = 'ambition_dashboard:screening_listboard_url'
