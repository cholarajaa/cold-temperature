# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class EventsDump(models.Model):
    '''To store raw dump of the events'''
    events_json = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(EventsDump, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.events_json


class UserData(models.Model):
    """To store user related data"""
    owner_name = models.CharField(max_length=256)
    company = models.CharField(max_length=256, null=False, blank=False)
    usertype = models.CharField(max_length=256, null=False, blank=False)
    partnerName = models.CharField(max_length=256, null=True, blank=True)
    segmentTypeDeparture = models.CharField(
        max_length=256, null=True, blank=True)
    functionalName = models.CharField(max_length=256, null=True, blank=True)
    partnerTypeStart = models.CharField(max_length=256, null=True, blank=True)
    bizLocationTypeStart = models.CharField(
        max_length=256, null=True, blank=True)
    packagingTypeCode = models.CharField(max_length=256, null=True, blank=True)
    tradeItemCountryOfOrigin = models.CharField(
        max_length=256, null=False, blank=False)
    lowTemp = models.IntegerField(null=False, blank=False)
    referenceTemp = models.IntegerField(null=False, blank=False)
    referenceLife = models.IntegerField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.owner_name, self.company, self.usertype)

    class Meta:
        unique_together = (
            'owner_name', 'company', 'usertype'
        )


class Event(models.Model):
    '''To store events'''
    time = models.DateTimeField(null=False, blank=False)
    organization_id = models.IntegerField(
        null=False, blank=False)
    raspberry_id = models.CharField(
        max_length=256, null=False, blank=False)
    event_type = models.CharField(
        max_length=256, null=False, blank=False)
    event_order = models.IntegerField(
        null=False, blank=False)
    is_current = models.BooleanField()
    elapsed_seconds = models.IntegerField(null=False, blank=False)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    client = models.CharField(max_length=256, null=True, blank=True)
    read_point = models.CharField(max_length=256, null=True, blank=True)
    biz_location = models.CharField(max_length=256, null=True, blank=True)
    biz_step = models.CharField(max_length=256, null=True, blank=True)
    version = models.IntegerField()
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s - %d - %s - %s - %d' % (
            self.time, self.organization_id, self.raspberry_id,
            self.event_type, self.event_order)

    class Meta:
        unique_together = (
            'time', 'organization_id', 'raspberry_id',
            'event_type', 'event_order'
        )


class AggergatedUserData(models.Model):
    """Aggregated data from UserData table"""
    company = models.CharField(max_length=256, null=False, blank=False)
    usertype = models.CharField(max_length=256, null=False, blank=False)
    lowTemp = models.FloatField(null=True, blank=True)
    referenceTemp = models.FloatField(null=True, blank=True)
    referenceLife = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return '%s - %s' % (
            self.company, self.usertype)

    class Meta:
        unique_together = ('company', 'usertype')
