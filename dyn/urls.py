from django.conf.urls.defaults import patterns

urlpatterns = patterns('dyn.views',
    (r'^update', 'update'),
)
