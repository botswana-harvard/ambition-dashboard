from .crf_model_wrapper import CrfModelWrapper


class RequisitionModelWrapper(CrfModelWrapper):

    model = 'ambition_subject.subjectrequisition'
    next_url_attrs = ['appointment', 'subject_identifier']
    querystring_attrs = ['subject_visit', 'panel_name']

    @property
    def appointment(self):
        try:
            return str(self.object.subject_visit.appointment.id)
        except AttributeError:
            return ''

    @property
    def subject_identifier(self):
        return self.object.subject_visit.subject_identifier
