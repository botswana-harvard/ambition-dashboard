from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from edc_consent import ConsentModelWrapperMixin
from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class SubjectScreeningModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    consent_model = 'ambition_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'ambition_subject.subjectscreening'
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
    querystring_attrs = ['gender']

    @property
    def html_reason(self):
        if not self.object.eligible:
            html = '<BR>'.join(self.object.reasons_ineligible.split(','))
            return mark_safe('<BR>'.join(['No:', html]))
        else:
            return 'Yes.'

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
        model_cls = django_apps.get_model(self.consent_model)
        try:
            consent = model_cls.objects.get(
                screening_identifier=self.object.screening_identifier)
        except ObjectDoesNotExist:
            consent = self.consent_object.model(**self.create_consent_options)
        return self.consent_model_wrapper_cls(model_obj=consent)
