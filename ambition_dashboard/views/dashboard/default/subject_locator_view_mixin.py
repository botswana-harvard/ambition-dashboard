from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from ....model_wrappers import SubjectLocatorModelWrapper


class SubjectLocatorViewMixin:

    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    subject_locator_model = 'bcpp_subject.subjectlocator'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject_locator = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            subject_locator=self.subject_locator_model_wrapper(
                model_obj=self.subject_locator))
        return context

    @property
    def subject_locator(self):
        """Returns a model instance either saved or unsaved.

        If a save instance does not exits, returns a new unsaved instance.
        """
        model_cls = django_apps.get_model(self.subject_locator_model)
        try:
            subject_locator = model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            subject_locator = model_cls(
                subject_identifier=self.subject_identifier)
        return subject_locator
