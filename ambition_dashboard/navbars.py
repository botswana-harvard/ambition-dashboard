from edc_navbar import NavbarItem, site_navbars, Navbar
from django.conf import settings


if settings.APP_NAME == 'ambition_dashboard':
    url_namespace = None
else:
    url_namespace = 'ambition_dashboard'

ambition_dashboard = Navbar(name='ambition_dashboard')

ambition_dashboard.append_item(
    NavbarItem(
        name='screened_subject',
        title='Screening',
        label='screening',
        fa_icon='fa-user-plus',
        url_name='screening_listboard_url',
        url_namespace=url_namespace))

ambition_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='subjects',
        fa_icon='fa-user-circle-o',
        url_name='listboard_url',
        url_namespace=url_namespace))

site_navbars.register(ambition_dashboard)
