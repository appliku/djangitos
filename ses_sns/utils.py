def get_permanent_bounced_emails_from_bounce_obj(bounce_obj: dict) -> list:
    """Extracts permanent bounced email addresses only as a list of strings.
    https://docs.aws.amazon.com/ses/latest/DeveloperGuide/notification-contents.html#bounce-object
    """
    bounced_recipients = bounce_obj.get("bouncedRecipients", list())
    return [br.get("emailAddress") for br in bounced_recipients if br.get("status").startswith("5")]


def get_emails_from_complaint_obj(complaint_obj: dict) -> list:
    """Extracts complaint email addresses from complaint_obj
    https://docs.aws.amazon.com/ses/latest/DeveloperGuide/notification-contents.html#complaint-object
    """
    return [cr.get("emailAddress") for cr in complaint_obj.get("complainedRecipients", list())]