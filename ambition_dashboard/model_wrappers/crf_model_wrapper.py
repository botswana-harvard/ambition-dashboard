from edc_subject_dashboard.model_wrappers import CrfModelWrapper as BaseCrfModelWrapper
from ambition_rando.treatment_description_mixin import TreatmentModelWrapperMixin


class CrfModelWrapper(TreatmentModelWrapperMixin, BaseCrfModelWrapper):

    querystring_attrs = ['subject_visit', 'regimen']
