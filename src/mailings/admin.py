from django.contrib import admin

from .models import MailingList


class MailingListAdmin(admin.ModelAdmin):
    pass


admin.site.register(MailingList, MailingListAdmin)
