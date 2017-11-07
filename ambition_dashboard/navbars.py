from edc_navbar import NavbarItem, site_navbars, Navbar

url_namespace = 'ambition_dashboard'

ambition_dashboard = Navbar(name='ambition_dashboard')

ambition_dashboard.append_item(
    NavbarItem(
        name='screened_subject',
        title='Screening',
        label='screening',
        fa_icon='fa-user-circle-o',
        url_name=f'{url_namespace}:screening_listboard_url'))

ambition_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='subjects',
        fa_icon='fa-user-circle-o',
        url_name=f'{url_namespace}:listboard_url'))

# ambition_dashboard.append_item(
#     NavbarItem(
#         name='lab',
#         title='edc_lab_dashboard',
#         glyphicon='fa-flask',
#         url_name=f'ambition:home_url'))

# register the navbar to the site
site_navbars.register(ambition_dashboard)
