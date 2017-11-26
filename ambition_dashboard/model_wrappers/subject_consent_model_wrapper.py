from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model = 'ambition_subject.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = [
        'screening_identifier', 'gender', 'first_name', 'initials', 'modified']
    subject_randomization_model = 'ambition_rando.subjectrandomization'

    @property
    def randomization_arm(self):
        model_cls = django_apps.get_model(self.subject_randomization_model)
        try:
            obj = model_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except ObjectDoesNotExist:
            rx_arm = None
        else:
            rx_arm = ' '.join(obj.rx.split('_')).title()
        return rx_arm
