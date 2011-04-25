#:coding=utf8:

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings
from django.test import TestCase

from beproud.django.notify.tests.base import TestBase

from beproud.django.notify.api import *

__all__ = ('MailNotifyTest',)

class MailNotifyTest(TestBase, TestCase):
    fixtures = ['test_users.json']
    
    def test_sending_mail(self):
        user = User.objects.get(pk=2)
        items_sent = notify(user, 'private_msg', extra_data={"spam": "eggs"})

        # 1 private_messages model
        # 1 news model
        # 1 private_messages mail
        self.assertEquals(items_sent, 3)

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, u'テストメール private_msg private_messages eggs')
        self.assertEquals(mail.outbox[0].body, u'Text メールボディ private_msg private_messages eggs\n')
