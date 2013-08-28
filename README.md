django-ddns
==========================

**django-ddns** implements the DynDNS protocol server-side as described on
http://dyn.com/support/developers/api/.

Architecture
------------

Main files:

    dyndns/
        settings.py: project settings
        settings_local.sample.py: sample settings to be completed and renamed
    dyn/
        views.py: view functions (no class-based views)
        libdyn.py: functions implementing the DynDNS protocol
    updaters/
        (update handlers)

