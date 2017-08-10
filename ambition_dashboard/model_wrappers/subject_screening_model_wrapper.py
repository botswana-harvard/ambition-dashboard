from django.apps import apps as django_apps
from edc_consent.model_wrappers import ConsentModelWrapperMixin
from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class SubjectScreeningModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    model = 'ambition_subject.subjectscreening'
    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').listboard_url_name
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['gender']

    consent_model_wrapper_cls = SubjectConsentModelWrapper

    def create_consent_options(self):
        options = super().create_consent_options
        options.update(subject_screening=self.object)
        return options
