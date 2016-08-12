# coding=utf-8

import datetime, time, os

import traceback as tb

from suds import WebFault

from django.db import connection, transaction
from django.utils import translation, timezone
from django.conf import settings
from django.core.cache import cache

from django.db.models import Q, F

from celery import group
from celery.task import periodic_task, task, Task, PeriodicTask
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from celery.exceptions import RetryTaskError, TaskRevokedError

from .models import soap_client

import logging
log = logging.getLogger(__name__)


RUN_BEFORE_CRONTAB = crontab(minute=int(settings.CRON_MIN) - 1, hour=settings.CRON_HOUR)
RUN_ALL_CRONTAB = crontab(minute=settings.CRON_MIN, hour=settings.CRON_HOUR) 
RUN_AFTER_CRONTAB = crontab(minute=int(settings.CRON_MIN) + 1, hour=settings.CRON_HOUR)


class SingleTask(Task):
    abstract = True

    # Custom
    lock_time = 3600
    cache = {}

    lang = {
        'ru': 'RU',
        'en': 'EN',
        'uk': 'UA',
        'fr': 'FR',
        'de': 'GR'
    }

    def append_local(self, cls, attr, prefix, val):
        obj = cls()
        attrs = {}
        for k, v in self.lang.items():
            if hasattr(obj, attr + '_' + k):
                attrs[attr + '_' + k] = val.get(prefix + '_' + v)

        return attrs

    def create_object(self, obj, uid, val, local=None, precache = True):

        # Caching
        cl_name = obj.__name__.lower()
        if precache and not self.cache.get(cl_name):
            cache = {}
            for item in obj.objects.all():
                cache.update({item.uid: item})
            self.cache.update({cl_name: cache})
        record, created = self.cache.get(cl_name, {}).get(uid), False

        # Localizing
        if local:
            for k, v in local[1].items():
                val.update(
                    self.append_local(obj, k, v, local[0])
                )

        # Creating and updating
        if record is None:
            record, created = obj.objects.get_or_create(uid = uid, defaults = val)
        if not created:
            modified = False
            for key in val.keys():
                value = val.get(key)
                if not modified:
                    try:
                        modified = not (value == getattr(record, key))
                    except:
                        modified = True
                setattr(record, key, value)
            if modified:
                record.save(update_fields=val.keys())
                try:
                    self.cache[cl_name][uid] = record
                except:
                    pass

        return record


    def after_return(self, *args, **kwargs):
        cache.delete(self.name)


    def run(self, **kwargs):

        self.cache = {}

        translation.activate('ru')
       
        key = self.name

        if cache.add(key, time.time()):
            res = self.go()

            return res
        else:
            when = cache.get(key)
            if time.time() - float(when) > self.lock_time:
                cache.add(key, time.time())
                res = self.go()

                return res

        raise RetryTaskError(when=datetime.datetime.now())

# Common

@task()
def delete_objects_by_ids(self, obj, ids):
    obj.objects.exclude(id__in = ids).update(status = 127)


@task()
def get_res_from_1c(self, command):
    try:
        client = soap_client()

        res = getattr(client.service, command)(settings.SITE_1C)
        if res and len(res):
            return resolve(res[0])
        else:
            return []

    except WebFault, f:
        raise Exception(f.fault)
    except Exception, e:
        raise Exception(tb.format_exc(100))


from suds.sudsobject import asdict

def resolve(res):
    if hasattr(res, '__keylist__'):
        ret = {}
        for k, v in asdict(res).iteritems():
            ret[k] = resolve(v)
        return ret
    elif isinstance(res, list):
        ret = []
        for i in res:
            ret.append(resolve(i))
        return ret
    elif isinstance(res, basestring):
        return res and unicode(res) or None
    else:
        return res
