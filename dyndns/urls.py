from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^nic/', include('dyn.urls')),
)
