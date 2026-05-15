from django.contrib import admin
from .models import *
for name, obj in list(globals().items()):
    if hasattr(obj, '_meta') and getattr(obj._meta, 'app_label', None):
        try: admin.site.register(obj)
        except admin.sites.AlreadyRegistered: pass
