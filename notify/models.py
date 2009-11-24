#:coding=utf8:
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from commons.model_fields import PickledObjectField, PositiveBigIntegerField
from account.models import User
import conf

class Notification(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'ユーザ'))
    notice_type = models.CharField(_(u'タイプ'), max_length=30, choices=conf.NOTICE_TYPES, db_index=True)
    media = models.CharField(_(u'メディア'), max_length=30, choices=conf.NOTICE_MEDIA, db_index=True)
    target_id = PositiveBigIntegerField(_(u'Target ID'), blank=True, null=True, db_index=True)
    origin_id = PositiveBigIntegerField(_(u'Origin ID'), blank=True, null=True, db_index=True)
    ctime = models.DateTimeField(_(u'作成日'), default=datetime.now)

    # pickleされたコンテキストデータ
    extra_data = PickledObjectField(editable=False, null=True, blank=True)

    @models.permalink
    def get_view_url(self):
        return ('view_notification' (), {
            'id': self.id,
        })
    
    def __unicode__(self):
        return "%s (%s, %s)" % (self.user.full_name, self.notice_type, self.media)

    class Meta:
       db_table=u'notifications'
       verbose_name=u'通達'
       verbose_name_plural=u'通知'
       ordering=('-ctime',)

class NotificationSetting(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'ユーザ'))
    notice_type = models.CharField(_(u'タイプ'), max_length=30, choices=conf.NOTICE_TYPES, db_index=True)
    media = models.CharField(_(u'メディア'), max_length=30, choices=conf.NOTICE_MEDIA, db_index=True)
    send = models.BooleanField(_(u'送信する？'))

    def __unicode__(self):
        return "%s (%s, %s)" % (self.user.full_name, self.notice_type, self.media)

    class Meta:
        db_table = u'notification_settings'
        verbose_name = _(u'通知設定')
        verbose_name_plural = _(u'通知設定')

# TODO: Mediaによってテーブルにコピーする？
