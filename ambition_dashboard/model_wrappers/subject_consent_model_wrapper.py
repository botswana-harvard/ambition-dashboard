from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model = 'ambition_subject.subjectconsent'
    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
    next_url_attrs = ['subject_identifier', ]
    querystring_attrs = [
        'gender', 'subject_screening', 'first_name', 'initials', 'modified']
    subject_randomization_model = 'ambition_subject.subjectrandomization'

    @property
    def subject_screening(self):
        try:
            return str(self.object.subject_screening.id)
        except AttributeError:
            return ''

    @property
    def subject_identifier(self):
        return str(self.object.subject_identifier)

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
