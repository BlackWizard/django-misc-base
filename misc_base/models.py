# coding=utf-8

from django.db import models

from django.utils.translation import ugettext_lazy as _

from positions.fields import PositionField

class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    cdate = models.DateTimeField(_(u'Created at'), auto_now_add=True)
    mdate = models.DateTimeField(_(u'Changed at'), auto_now=True)

    class Meta:
        abstract = True

STATUS = (
    (0, _(u'Active')),
    (1, _(u'Editing')),
    (127, _(u'Deleted')),
)

class BaseStatusModel(models.Model):
    status = models.PositiveSmallIntegerField(_(u'Status'), max_length=3, choices=STATUS, default=0, db_index=True)

    class Meta:
        abstract = True

class BaseNameModel(models.Model):
    name = models.CharField(_(u'Title'), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True

class BaseSlugModel(models.Model):
    slug = models.SlugField(_(u'Slug'), max_length=255, null=True, blank=True, db_index=True)

    class Meta:
        abstract = True


class BaseDetailModel(models.Model):
    detail = models.TextField(_(u'Detail'),  null=True, blank=True)

    class Meta:
         abstract = True

class BaseSEOModel(models.Model):
    tt = models.TextField(_(u'Title in meta'), blank=True, null=True)
    kw = models.TextField(_(u'Keywords'), blank=True, null=True)
    ds = models.TextField(_(u'Description'), blank=True, null=True)
    ft = models.TextField(_(u'SEO text'), blank=True, null=True)

    class Meta:
        abstract = True

class BasePositionModel(models.Model):
     order = PositionField(verbose_name=_(u'Position'))

     class Meta:
         ordering = ('order', )
         abstract = True

class BaseUIDModel(BaseModel, BaseNameModel):
    uid = models.CharField(_('UID'), max_length=16, db_index=True, unique=True, null = True, blank = True)

    class Meta:
        abstract = True

class BaseUIDPositionModel(BaseUIDModel, BasePositionModel):

    class Meta(BasePositionModel.Meta):
        abstract = True
