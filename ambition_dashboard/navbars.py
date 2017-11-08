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
        fa_icon='fa-user-circle-o',
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

# ambition_dashboard.append_item(
#     NavbarItem(
#         name='lab',
#         title='edc_lab_dashboard',
#         glyphicon='fa-flask',
#         url_name=f'ambition:home_url'))

# register the navbar to the site
site_navbars.register(ambition_dashboard)
