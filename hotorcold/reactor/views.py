# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view
from reactor.models import Event
from reactor.serializers import EventSerializer, EventsDumpSerializer
from reactor.tasks import create_event, update_aggregated_userdata


class EventViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing Event instances.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request):
        import pdb;pdb.set_trace()
        data = {
            'events_json': request.data
        }
        serializer = EventsDumpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_event.apply_async((request.data,))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('GET',))
def aggregate_user_data(request):
    update_aggregated_userdata.apply_async()
    return Response({"message": "Success"}, status=status.HTTP_200_OK)


def index(request):
    return HttpResponse('Hello reactor!!!')
