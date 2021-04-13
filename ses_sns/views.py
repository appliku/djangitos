import json
import logging
from django.http import HttpRequest, HttpResponse

from django.views.generic.base import View
from rest_framework import status

from ses_sns.models import SNSNotification

logger = logging.getLogger(__name__)


class ReceiveSNSNotification(View):
    """Receives a message from SNS and stores to db"""

    def post(self, request: HttpRequest, *args, **kwargs):
        http_headers = {i[0]: i[1] for i in request.META.items() if i[0].startswith('HTTP_')}
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            SNSNotification.objects.create(data=body, headers=http_headers).process()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(f"Exception during processing SNS Notification {e}")
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)