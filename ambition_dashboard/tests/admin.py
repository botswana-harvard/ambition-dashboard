from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import SubjectConsent, SubjectLocator, Appointment
from .models import SubjectRequisition, SubjectVisit


class AdminSite(DjangoAdminSite):
    site_title = 'Ambition Subject'
    site_header = 'Ambition Subject'
    index_title = 'Ambition Subject'
    site_url = '/ambition_subject/list/'


ambition_subject_admin = AdminSite(name='ambition_subject_admin')

ambition_subject_admin.register(SubjectConsent)
ambition_subject_admin.register(SubjectLocator)
ambition_subject_admin.register(Appointment)
ambition_subject_admin.register(SubjectVisit)
ambition_subject_admin.register(SubjectRequisition)
