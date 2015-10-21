from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from .forms import TelnetInputForm
from .tasks import configure_batch, email_admin
from celery import chord
import celery
import json


try:
    stats = celery.current_app.control.inspect().stats()
    NO_OF_WORKERS = stats[stats.keys()[0]]['pool']['max-concurrency']
except KeyError:
    NO_OF_WORKERS = None


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['workers_count'] = NO_OF_WORKERS

        return context


class CommandExecutionView(View):
    def post(self, request, *args, **kwargs):
        form = TelnetInputForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                json.dumps({'success': False, 'validation_error': True, 'message': form.errors, 'form_error': True}),
                content_type="application/json", status=200)

        params = [(ip, form.cleaned_data['commands'],
                         form.cleaned_data['username'], form.cleaned_data['password'],
                   form.cleaned_data['python_shell']) for ip in form.cleaned_data['ips']]

        res = chord((configure_batch.s(*param) for param in params), email_admin.s(form.cleaned_data['admin_email']))
        res.apply_async()

        return HttpResponse(json.dumps({'success': True}),
                            content_type='application/json', status=200)
