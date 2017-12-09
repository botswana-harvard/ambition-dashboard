from django.test import TestCase
from edc_base.utils import get_utcnow

from ..views import SubjectDashboardView
from .models import Appointment, SubjectVisit, BloodResultModel
from .models import DeathReport, SubjectOffstudy, StudyTerminationConclusion


class TestOffStudyRequired(TestCase):

    def setUp(self):
        self.appointment = Appointment.objects.create(
            subject_identifier='12345',
            visit_code='1000',
            appt_datetime=get_utcnow())
        self.subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            subject_identifier='11111',
            visit_code='1000')
        self.blood_result_model = BloodResultModel.objects.create(
            subject_visit=self.subject_visit, alt=120, absolute_neutrophil=0.8,
            platelets=60)
        self.study_termination_model = StudyTerminationConclusion.objects.create(
            subject_identifier='11111')
        self.death_report_model = DeathReport.objects.create(
            subject_identifier='11111')

    def test_is_eligible(self):
        """Assert subject is eligible based on their blood results.
        """
        dashboard_view = SubjectDashboardView()
        dashboard_view.subject_identifier = '11111'
        dashboard_view.blood_result_model = BloodResultModel._meta.label_lower
        self.assertTrue(dashboard_view.is_eligible)

    def test_is_eligible_abnormal_blood_results_invalid(self):
        """Assert subject is ineligible if they abnormal blood results.
        """
        dashboard_view = SubjectDashboardView()
        dashboard_view.subject_identifier = '12345'
        self.blood_result_model = BloodResultModel.objects.create(
            subject_visit=self.subject_visit, alt=300, absolute_neutrophil=0.1,
            platelets=60)
        dashboard_view.blood_result_model = BloodResultModel._meta.label_lower
        self.assertFalse(dashboard_view.is_eligible)

    def test_offstudy_form_required(self):
        dashboard_view = SubjectDashboardView()
        dashboard_view.blood_result_model = BloodResultModel._meta.label_lower
        dashboard_view.subject_identifier = '11111'
        dashboard_view.study_termination_model = (
            StudyTerminationConclusion._meta.label_lower)
        dashboard_view.death_report_model = DeathReport._meta.label_lower
        self.assertTrue(dashboard_view.offstudy_required)

    def test_offstudy_form_required_exists(self):
        """Assert offstudy form will not be required if it already exists.
        """
        dashboard_view = SubjectDashboardView()
        SubjectOffstudy.objects.create(subject_identifier='11111')
        dashboard_view.blood_result_model = BloodResultModel._meta.label_lower
        dashboard_view.subject_identifier = '11111'
        dashboard_view.subject_offstudy_model = SubjectOffstudy._meta.label_lower
        dashboard_view.study_termination_model = (
            StudyTerminationConclusion._meta.label_lower)
        dashboard_view.death_report_model = DeathReport._meta.label_lower
        self.assertFalse(dashboard_view.offstudy_required)
