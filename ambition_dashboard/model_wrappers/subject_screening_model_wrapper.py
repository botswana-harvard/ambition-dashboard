from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_consent import ConsentModelWrapperMixin
from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class SubjectScreeningModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'ambition_screening.subjectscreening'
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
    querystring_attrs = ['gender']

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent(self):
        """Returns a wrapped saved or unsaved consent.
        """
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            consent_model_obj = consent_model_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except ObjectDoesNotExist:
            consent_model_obj = consent_model_cls(
                **self.create_consent_options)
        return self.consent_model_wrapper_cls(model_obj=consent_model_obj)
