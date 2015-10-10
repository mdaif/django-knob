from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from .forms import TelnetInputForm
from .tasks import configure_batch, email_admin
from multiprocessing import cpu_count
from .helpers import chunks
from multiprocessing import Pool
import logging
import json
import math




class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['workers_count'] = cpu_count()

        return context


class CommandExecutionView(View):
    def post(self, request, *args, **kwargs):
        form = TelnetInputForm(request.POST)
        if not form.is_valid():
            return HttpResponse(
                json.dumps({'success': False, 'validation_error': True, 'message': form.errors, 'form_error': True}),
                content_type="application/json", status=200)

        ip_chunks = chunks(form.cleaned_data['ips'], cpu_count(), form.cleaned_data['commands'], form.cleaned_data['username'], form.cleaned_data['password'], form.cleaned_data['python_shell'])

        workers = Pool(5)
        email_admin.email = form.cleaned_data['admin_email']  # monkey patching the emaiL_admin function to pass the admin's email parameter .. I know ugly as hell
        email_admin.pool = workers

        workers.map_async(configure_batch, ip_chunks, callback=email_admin)

        return HttpResponse(json.dumps({'success': True}), content_type='application/json', status=200)
