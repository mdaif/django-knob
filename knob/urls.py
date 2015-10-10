from django.conf.urls import url
from .views import HomePageView, CommandExecutionView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^commands/execute/?$', CommandExecutionView.as_view(), name='exec_command')
]
