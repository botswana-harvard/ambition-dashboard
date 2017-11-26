from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_subject_dashboard.model_wrappers import CrfModelWrapper as BaseCrfModelWrapper


class CrfModelWrapper(BaseCrfModelWrapper):

    querystring_attrs = ['subject_visit', 'regimen']
    subject_randomization_model = 'ambition_rando.subjectrandomization'

    @property
    def regimen(self):
        model_cls = django_apps.get_model(self.subject_randomization_model)
        try:
            obj = model_cls.objects.get(
                subject_identifier=self.object.subject_visit.appointment.subject_identifier)
        except ObjectDoesNotExist:
            rx_arm = None
        else:
            rx_arm = ' '.join(obj.rx.split('_')).title()
        return rx_arm
