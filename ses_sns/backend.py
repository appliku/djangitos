import logging
from collections import OrderedDict
from email.mime.base import MIMEBase
from email.utils import parseaddr

from django.core.files.base import ContentFile
from post_office import EmailBackend

from post_office.settings import get_default_priority
from ses_sns.models import BlacklistedEmail

logger = logging.getLogger(__name__)


def filter_blacklisted_recipients(addresses):
    """Remove blacklisted emails from addresses"""
    if type(addresses) is str:
        addr = parseaddr(addresses)[1]
        if not BlacklistedEmail.objects.filter(email=addr).exists():
            return addresses
        return []
    if type(addresses) is list:
        filtered_addresses = []
        for recipient in addresses:
            addr = parseaddr(recipient)[1]
            logger.debug(f"Address in check for blacklist: {addr}")
            if BlacklistedEmail.objects.filter(email=addr).exists():
                continue
            filtered_addresses.append(recipient)
        return filtered_addresses


class FilteringEmailBackend(EmailBackend):

    def open(self):
        pass

    def close(self):
        pass

    def send_messages(self, email_messages):
        """
        Queue one or more EmailMessage objects and returns the number of
        email messages sent.
        """
        from post_office.mail import create
        from post_office.utils import create_attachments

        if not email_messages:
            return

        for email_message in email_messages:
            subject = email_message.subject
            from_email = email_message.from_email
            headers = email_message.extra_headers
            message = email_message.message()

            # Look for first 'text/plain' and 'text/html' alternative in email
            plaintext_body = html_body = ''
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    plaintext_body = part.get_payload()
                    if html_body:
                        break
                if part.get_content_type() == 'text/html':
                    html_body = part.get_payload()
                    if plaintext_body:
                        break

            attachment_files = {}
            for attachment in email_message.attachments:
                if isinstance(attachment, MIMEBase):
                    attachment_files[attachment.get_filename()] = {
                        'file': ContentFile(attachment.get_payload()),
                        'mimetype': attachment.get_content_type(),
                        'headers': OrderedDict(attachment.items()),
                    }
                else:
                    attachment_files[attachment[0]] = ContentFile(attachment[1])
            recipients = filter_blacklisted_recipients(email_message.to)
            cc = filter_blacklisted_recipients(email_message.cc)
            bcc = filter_blacklisted_recipients(email_message.bcc)
            if not len(recipients + cc + bcc):
                continue
            email = create(sender=from_email,
                           recipients=recipients,
                           cc=cc,
                           bcc=bcc,
                           subject=subject,
                           message=plaintext_body,
                           html_message=html_body,
                           headers=headers)

            if attachment_files:
                attachments = create_attachments(attachment_files)

                email.attachments.add(*attachments)

            if get_default_priority() == 'now':
                email.dispatch()
