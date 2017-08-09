from django.test import TestCase, tag
from edc_model_wrapper.tests import ModelWrapperTestHelper

from ..model_wrappers import AppointmentModelWrapper
from ..model_wrappers import SubjectConsentModelWrapper
from ..model_wrappers import SubjectLocatorModelWrapper
from .models import SubjectScreening, Appointment, SubjectVisit
from ..model_wrappers import SubjectVisitModelWrapper
from ..model_wrappers import RequisitionModelWrapper


class TestModelWrappers(TestCase):

    model_wrapper_helper_cls = ModelWrapperTestHelper

    @tag('1')
    def test_subject_consent(self):
        subject_screening = SubjectScreening.objects.create(
            screening_identifier='1234')
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectConsentModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345',
            subject_screening=subject_screening)
        helper.test(self)

    @tag('1')
    def test_subject_locator(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectLocatorModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345')
        helper.test(self)

    @tag('1')
    def test_appointment(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=AppointmentModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345')
        helper.test(self)

    @tag('1')
    def test_subject_visit(self):
        appointment = Appointment.objects.create(
            subject_identifier='092-12345',)
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectVisitModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345',
            appointment=appointment)
        helper.test(self)

    @tag('1')
    def test_subject_requisition(self):
        appointment = Appointment.objects.create(
            subject_identifier='092-12345')
        subject_visit = SubjectVisit.objects.create(
            subject_identifier='092-12345',
            appointment=appointment)
        helper = self.model_wrapper_helper_cls(
            model_wrapper=RequisitionModelWrapper,
            app_label='ambition_dashboard',
            subject_visit=subject_visit)
        helper.test(self)
