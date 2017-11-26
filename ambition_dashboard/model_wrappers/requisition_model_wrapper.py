from edc_subject_dashboard.model_wrappers import CrfModelWrapper


class RequisitionModelWrapper(CrfModelWrapper):

    model = 'ambition_subject.subjectrequisition'
    requisition_panel_name = None
    querystring_attrs = ['subject_visit', 'panel_name']

    @property
    def panel_name(self):
        return self.requisition_panel_name
