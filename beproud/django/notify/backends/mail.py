#:coding=utf-8:

from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection, EmailMessage, EmailMultiAlternatives
from django.conf import settings

from beproud.django.notify.backends.base import BaseBackend

class EmailBackend(BaseNotify):
    """
    A backend that sends email for the given notification type.

    The email content is rendered from a template found in the
    following templates:

    notify/<notice_type>/<media>/mail_subject.txt
    notify/<notice_type>/<media>/mail_body.html
    notify/<notice_type>/<media>/mail_body.txt

    The body templates can contain both html and text, only html, or only text.
    The EmailBackend does the following:

    The email recipient is retrieved from each target object by searching for a
    "email" or "mail" property. If none is found the extra_data dictionary is
    searched for a "email" or "mail" key.

    If no recipient email could be retrieved or a subject template could not
    be found then the mail is not sent.

    If only a text template is found then the email is sent as text.
    If only a html template is found then the email is send as multipart with a
    text body created by stripping html tags from the html body.
    If both html and a text template are found then the email is sent as multipart
    with the rendered content.
    """
    def send(targets, notice_type, media, extra_data={}):
        subject_template = 'notify/%s/%s/mail_subject.txt' % (notice_type, media)
        body_html_template = 'notify/%s/%s/mail_body.html' % (notice_type, media)
        body_text_template = 'notify/%s/%s/mail_body.txt' % (notice_type, media)

        messages = []
    
        try:
            for target in targets:
                to_email = getattr(target, 'email', getattr(target, 'mail', extra_data.get('email', extra_data.get('mail'))))
                if to_email:
                        context = {
                            'target': target,
                            'notice_type': notice_type,
                            'media': media,
                        }
                        context.update(extra_data)

                        subject = render_to_string(subject_template, context)

                        try:
                            body_html = render_to_string(body_html_template, context)
                        except TemplateDoesNotExist, e:
                            body_html = None
                    
                        try:
                            body_text = render_to_string(body_text_template, context)
                        except TemplateDoesNotExist, e:
                            body_text = None

                        if body_html and not body_text:
                            body_text = strip_tags(body_html)

                        if body_text and body_html:
                            # HTML mail
                            message = EmailMultiAlternatives(subject, body_text, to=[to_email])
                            message.attach_alternative(body_html, "text/html")
                            messages.append(message)
                        elif body_text:
                            # Normal Text Mail
                            messages.append(EmailMessage(subject, body_text, to=[to_email]))
        except TemplateDoesNotExist, e:
            # Subject template does not exist.

            # TODO: logging
            pass

        connection = get_connection(fail_silently=True)
        return connection.send_messages(messages)