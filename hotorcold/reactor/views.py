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
from reactor.tasks import create_or_update_event_data


class EventViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing Event instances.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request):
        data = {
            'events_json': request.data
        }
        serializer = EventsDumpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            create_or_update_event_data.apply_async((request.data,))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        if pk:
            Event.objects.get(pk=pk).delete()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)


def index(request):
    return HttpResponse('Hello reactor!!!')
