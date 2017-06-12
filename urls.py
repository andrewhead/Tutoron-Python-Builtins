from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.modules.python_builtins.views.scan', name='scan'),
    url(r'^explain$', 'tutorons.modules.python_builtins.views.explain', name='explain'),
)
