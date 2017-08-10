import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_dashboard.views import ListboardView

from ...model_wrappers import SubjectScreeningModelWrapper


class ListBoardView(AppConfigViewMixin, EdcBaseViewMixin, ListboardView):

    model = 'ambition_subject.subjectscreening'
    model_wrapper_cls = SubjectScreeningModelWrapper
    listboard_url_name = django_apps.get_app_config(
        'ambition_dashboard').screening_listboard_url_name
    paginate_by = 10
    app_config_name = 'ambition_dashboard'
    ordering = '-modified'

    navbar_item_selected = 'screened_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_template_names(self):
        return [django_apps.get_app_config(
            self.app_config_name).screening_listboard_template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('get_absolute_url', self.model_cls().get_absolute_url())
        context.update(
            subject_screening_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
