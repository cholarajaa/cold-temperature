# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from hotorcold.celery import app as celery_app
from reactor.serializers import EventSerializer, UserDataSerializer
from reactor.models import Event, UserData, AggregatedUserData
from collections import Counter
from django.db.models import Avg


@celery_app.task(name='create_event', ignore_result=True)
def create_event(event_data):
    '''this is celery task to create event from dict'''
    event_dict = json.loads(event_data)
    user_data = event_dict['user_data']
    if type(user_data) != dict:
        user_data = json.loads(user_data)
    userdata_set = UserData.objects.filter(
        owner_name=user_data.get('owner_name', None),
        company=user_data.get('company', None),
        usertype=user_data.get('usertype', None)
    )
    if not userdata_set:
        user_serializer = UserDataSerializer(data=user_data)
        if user_serializer.is_valid():
            user_ins = user_serializer.save()
        else:
            return user_data
    else:
        user_serializer = UserDataSerializer(
            userdata_set.first(), data=user_data)
        if user_serializer.is_valid():
            user_ins = user_serializer.save()
        else:
            return user_serializer.errors
    event_dict['user_data'] = user_ins.id

    event = Event.objects.filter(
        time=event_dict.get('time', None),
        organization_id=event_dict.get('organization_id', None),
        raspberry_id=event_dict.get('raspberry_id', None),
        event_type=event_dict.get('event_type', None),
        event_order=event_dict.get('event_order', None)
    )
    if event:
        event_serializer = EventSerializer(
            instance=event.first(), data=event_dict)
        if event_serializer.is_valid():
            event_serializer.save()
            return event_serializer.data
    else:
        event_serializer = EventSerializer(data=event_dict)
        if event_serializer.is_valid():
            event_serializer.save()
            return event_serializer.data
    return event_serializer.errors


# convert this to 60 mins periodical task to update userdata
@celery_app.task(name='agreegate_userdata', ignore_result=True)
def update_aggregated_userdata():
    for c, u in list(Counter(UserData.objects.values_list(
        'company', 'usertype'))):
        comp_n_type = UserData.objects.filter(company=c, usertype=u)
        aggregated_dict = comp_n_type.aggregate(
            Avg('lowTemp'), Avg('referenceTemp'), Avg('referenceLife'))
        AggregatedUserData.objects.update_or_create(
            company=c,
            usertype=u,
            defaults={
                "lowTemp": aggregated_dict['lowTemp__avg'],
                "referenceTemp": aggregated_dict['referenceTemp__avg'],
                "referenceLife": aggregated_dict['referenceLife__avg']
            }
        )
    return True
