from django.contrib import admin

from .models import *


admin.site.register(Collection)
admin.site.register(DataFile)
admin.site.register(Document)
admin.site.register(DocumentXMPMeta)
admin.site.register(Term)
