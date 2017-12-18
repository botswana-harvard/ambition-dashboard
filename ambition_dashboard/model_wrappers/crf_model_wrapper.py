from edc_subject_dashboard.model_wrappers import CrfModelWrapper as BaseCrfModelWrapper


class CrfModelWrapper(BaseCrfModelWrapper):

    querystring_attrs = ['subject_visit']
