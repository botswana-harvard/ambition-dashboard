from django.apps import apps as django_apps
from edc_model_wrapper import ModelWrapper
from django.core.exceptions import ObjectDoesNotExist


class CrfModelWrapper(ModelWrapper):

    next_url_name = django_apps.get_app_config(
        'ambition_dashboard').dashboard_url_name
    next_url_attrs = ['appointment', 'subject_identifier']
    querystring_attrs = ['subject_visit', 'regimen']
    subject_randomization_model = 'ambition_rando.subjectrandomization'

    @property
    def subject_visit(self):
        return str(self.object.subject_visit.id)

    @property
    def appointment(self):
        return str(self.object.subject_visit.appointment.id)

    @property
    def subject_identifier(self):
        return self.object.subject_visit.subject_identifier

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
