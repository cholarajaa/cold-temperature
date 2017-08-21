# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from reactor.models import Event, UserData


class ModelsTestCase(TestCase):
    """
    This class defines the test suite for
    the Notification model
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
        Test Notification model can create a Notificaiton
        """
        user_data_id = UserData.objects.create(
            owner_name="someOwner",
            company="someCompany",
            usertype="superUser",
            lowTemp="10",
            referenceTemp="15",
            tradeItemCountryOfOrigin="centaury"
        )
        old_count = Event.objects.count()
        Event(
            event_type="FTGroupEvent",
            user_data=user_data_id,
            organization_id=108244,
            elapsed_seconds=68,
            is_current=0,
            event_order=3418470,
            raspberry_id=116503,
            read_point="aLDdltowLayzKTMzVqP",
            biz_location="PyogreZQyyqUlAnYbWEQ",
            client="goAvACuDoSJvDRsJdKHa",
            company_name="ehWsztVkVcJiuTitBybd",
            version=26,
            time="2017-08-18T16:13:40.673455Z",
            biz_step="IHCivekocFRrLmadh"
        ).save()
        new_count = Event.objects.count()
        self.assertNotEqual(old_count, new_count)


    def test_model_can_create_UserData(self):
        pass

    def test_model_can_create_AggregatedUserData(self):
        pass

    def test_model_can_create_EventsDump(self):
        pass