from django.urls import path

from django.views.decorators.csrf import csrf_exempt

from ses_sns.views import ReceiveSNSNotification

urlpatterns = [
    path("sns_url", csrf_exempt(ReceiveSNSNotification.as_view()), name="sns_url"),
]