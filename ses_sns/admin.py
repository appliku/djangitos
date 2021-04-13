
from django.contrib import admin
from ses_sns.models import SNSNotification, BlacklistedEmail


class SNSNotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(SNSNotification, SNSNotificationAdmin)


class BlacklistedEmailAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlacklistedEmail, BlacklistedEmailAdmin)