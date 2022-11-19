from django.contrib import admin
from .models import Message


class MessageListAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageListAdmin)
