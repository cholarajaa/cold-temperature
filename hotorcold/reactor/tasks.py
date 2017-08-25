# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from hotorcold.celery import app as celery_app
from reactor.serializers import EventSerializer, UserDataSerializer
from reactor.models import Event, UserData, AggregatedUserData
from collections import Counter
from django.db.models import Avg
from celery.utils.log import get_logger

logger = get_logger(__name__)


@celery_app.task(name='process_data', ignore_result=True)
def create_or_update_event_data(event_json):
    """chaining data handling"""
    event_dict = json.loads(event_json)
    chain = create_event.s(event_dict) | create_user.s(event_dict) |\
        aggregate_userdata.s()
    chain()


@celery_app.task(name='create_user')
def create_user(event_id, event_dict):
    user_data = event_dict['user_data']
    user_data['event'] = Event.objects.filter(pk=event_id)
    userdata_set = UserData.objects.filter(
        owner_name=user_data.get('owner_name', None),
        company=user_data.get('company', None),
        usertype=user_data.get('usertype', None)
    )
    if not userdata_set:
        user_serializer = UserDataSerializer(data=user_data)
        if user_serializer.is_valid():
            user_ins = user_serializer.save()
            return user_ins.company, user_ins.usertype
        else:
            logger.info(
                'user data serializer failed %s' % user_serializer.errors)
            return user_serializer.errors
    else:
        user_serializer = UserDataSerializer(
            userdata_set.first(), data=user_data)
        if user_serializer.is_valid():
            user_ins = user_serializer.save()
            return user_ins.company, user_ins.usertype
        else:
            logger.info(
                'user data serializer failed %s' % user_serializer.errors)
            return user_serializer.errors


@celery_app.task(name='create_event')
def create_event(event_dict):
    event = Event.objects.filter(
        time=event_dict.get('time', None),
        organization_id=event_dict.get('organization_id', None),
        raspberry_id=event_dict.get('raspberry_id', None),
        event_type=event_dict.get('event_type', None),
        event_order=event_dict.get('event_order', None)
    )
    event_dict.pop('user_data')
    if event:
        event_serializer = EventSerializer(
            instance=event.first(), data=event_dict)
        if event_serializer.is_valid():
            event = event_serializer.save()
            return event.id
    else:
        logger.info('processing event failed %s' % event_dict)
        event_serializer = EventSerializer(data=event_dict)
        if event_serializer.is_valid():
            event = event_serializer.save()
            return event.id
    logger.info(
        'Event serializer failed %s' % event_serializer.errors)
    return event_serializer.errors


@celery_app.task(name='aggregate_userdata', ignore_result=True)
def aggregate_userdata(user_data):
    company, usertype = user_data
    logger.info(user_data)
    comp_n_type = UserData.objects.filter(company=company, usertype=usertype)
    aggregated_dict = comp_n_type.aggregate(
        Avg('lowTemp'), Avg('referenceTemp'), Avg('referenceLife'))
    AggregatedUserData.objects.update_or_create(
        company=company,
        usertype=usertype,
        defaults={
            "lowTemp": aggregated_dict["lowTemp__avg"],
            "referenceTemp": aggregated_dict["referenceTemp__avg"],
            "referenceLife": aggregated_dict["referenceLife__avg"],
            "partnerName": Counter(list(comp_n_type.values_list(
                "partnerName", flat=True))),
            "segmentTypeDeparture": Counter(list(
                comp_n_type.values_list(
                    "segmentTypeDeparture", flat=True))),
            "functionalName": Counter(list(comp_n_type.values_list(
                "functionalName", flat=True))),
            "partnerTypeStart": Counter(list(comp_n_type.values_list(
                "partnerTypeStart", flat=True))),
            "bizLocationTypeStart": Counter(list(
                comp_n_type.values_list(
                    "bizLocationTypeStart", flat=True))),
            "packagingTypeCode": Counter(list(comp_n_type.values_list(
                "packagingTypeCode", flat=True))),
            "tradeItemCountryOfOrigin": Counter(list(
                comp_n_type.values_list(
                    "tradeItemCountryOfOrigin", flat=True))),
            "owner_name": Counter(list(comp_n_type.values_list(
                "owner_name", flat=True)))
        }
    )
    return True
