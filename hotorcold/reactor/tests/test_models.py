# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from reactor.models import Event, UserData, EventsDump, AggregatedUserData
from django.db.utils import IntegrityError
from mixer.backend.django import mixer


class ModelsTestCase(TestCase):
    """
    This class defines the test suite for
    the Event model
    """

    def setUp(self):
        """Define Model variables"""
        self.event_dict = {
            "event_type": "FTGroupEvent",
            "user_data": {
                "partnerName": "qnDxLiOtZpuVszsuqPAo",
                "referenceLife": 38,
                "owner_name": "rEZvvEluhHcAboGIhMxghWDAOOndXTceKxYRIiYL",
                "company": "blmkfigKORKJriwICsxLaOWnHOsBMK",
                "usertype": "Storage",
                "segmentTypeDeparture": "mmKmsSnXIbkXLZvDUclf",
                "tradeItemCountryOfOrigin": "vaNnlzIzVQGhrpqXyykOYZMiKeJlVl",
                "functionalName": "PhhwiZSxggxhAtsdNrAW",
                "lowTemp": 29,
                "partnerTypeStart": "DrocqRoBsPOevFILyiP",
                "referenceTemp": 44,
                "bizLocationTypeStart": "UBSJhKffzfDchgtFGDat",
                "packagingTypeCode": "vGPiRTsYBBXGEBsLSqTL"
            },
            "organization_id": 108244,
            "elapsed_seconds": 68,
            "is_current": 0,
            "event_order": 3418470,
            "raspberry_id": "116503",
            "read_point": "aLDdltowLayzKTMzVqP",
            "biz_location": "PyogreZQyyqUlAnYbWEQ",
            "client": "goAvACuDoSJvDRsJdKHa",
            "company_name": "ehWsztVkVcJiuTitBybd",
            "version": 26,
            "time": "2017-08-18T16:13:40.673455Z",
            "biz_step": "IHCivekocFRrLmadh"
        }

    def test_model_can_create_Event(self):
        """
        Test Event model can create an Event instance
        """
        old_count = Event.objects.count()
        mixer.blend('reactor.event')
        new_count = Event.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_create_UserData(self):
        """
        Test UserData model can create a UserData instance
        """
        self.assertEqual(UserData.objects.count(), 0)
        user = mixer.blend('reactor.userdata')
        self.assertEqual(UserData.objects.count(), 1)
        try:
            user = mixer.blend(
                'reactor.userdata', owner_name=user.owner_name,
                company=user.company, usertype=user.usertype
            )
        except Exception as e:
            self.assertEqual('duplicate key value violates unique constraint' in e.message, True)

    def test_model_can_create_AggregatedUserData(self):
        """
        Test AggregatedUserData model can create a AggregatedUserData instance
        """
        self.assertEqual(AggregatedUserData.objects.count(), 0)
        mixer.blend('reactor.aggregateduserdata')
        self.assertEqual(AggregatedUserData.objects.count(), 1)

    def test_model_can_create_EventsDump(self):
        """
        Test EventsDump model can create a EventsDump instance
        """
        self.assertEqual(EventsDump.objects.count(), 0)
        EventsDump.objects.create(events_json=self.event_dict)
        self.assertEqual(EventsDump.objects.count(), 1)
