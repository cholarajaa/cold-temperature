# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from reactor.models import EventsDump


class EventViewSetTestCase(TestCase):
    """Test suite for api views."""

    def setUp(self):
        """
        Define the test client and notification data
        """
        self.client = APIClient()
        self.event_data = json.dumps({
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
        })

    def test_api_can_create_event(self):
        """
        Test the api has notification created.
        """
        import pdb;pdb.set_trace()
        self.response = self.client.post(
            '/api/events/',
            self.event_data,
            format="json")
        self.assertEqual(
            EventsDump.objects.count(), 1)
        self.assertEqual(
            self.response.status_code,
            status.HTTP_200_OK
        )
