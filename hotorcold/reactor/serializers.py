from rest_framework import serializers
from reactor.models import Event, UserData, EventsDump


class EventsDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsDump
        fields = '__all__'


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.partnerName = validated_data.get(
            'partnerName', instance.partnerName)
        instance.segmentTypeDeparture = validated_data.get(
            'segmentTypeDeparture', instance.segmentTypeDeparture)
        instance.functionalName = validated_data.get(
            'functionalName', instance.functionalName)
        instance.partnerTypeStart = validated_data.get(
            'partnerTypeStart', instance.partnerTypeStart)
        instance.bizLocationTypeStart = validated_data.get(
            'bizLocationTypeStart', instance.bizLocationTypeStart)
        instance.packagingTypeCode = validated_data.get(
            'packagingTypeCode', instance.packagingTypeCode)
        instance.tradeItemCountryOfOrigin = validated_data.get(
            'tradeItemCountryOfOrigin', instance.tradeItemCountryOfOrigin)
        instance.lowTemp = validated_data.get('lowTemp', instance.lowTemp)
        instance.referenceTemp = validated_data.get(
            'referenceTemp', instance.referenceTemp)
        instance.referenceLife = validated_data.get(
            'referenceLife', instance.referenceLife)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.get('user_data')
        user_ser = UserDataSerializer(data=user_data)
        if user_ser.is_valid():
            user_data = user_ser.save()
        validated_data['user_data'] = user_data
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        instance.read_point = validated_data.get(
            'read_point', instance.read_point)
        instance.version = validated_data.get(
            'version', instance.version)
        instance.biz_location = validated_data.get(
            'biz_location', instance.biz_location)
        instance.elapsed_seconds = validated_data.get(
            'elapsed_seconds', instance.elapsed_seconds)
        instance.client = validated_data.get('client', instance.client)
        instance.is_current = validated_data.get(
            'is_current', instance.is_current)
        instance.biz_step = validated_data.get(
            'biz_step', instance.biz_step)
        instance.company_name = validated_data.get(
            'company_name', instance.company_name)
        instance.save()
        return instance
