from rest_framework import serializers

from main.models import Airplane, Person, Ticket, Country


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')
    arrival_time = serializers.DateTimeField(format='%d-%m-%Y %H:%M:%S')

    class Meta:
        model = Ticket
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['person'] = PersonSerializer(instance.person).data
        representation['origin'] = CountrySerializer(instance.origin).data
        representation['destination'] = CountrySerializer(instance.destination).data
        representation['airplane'] = AirplaneSerializer(instance.airplane).data
        representation['image'] = self._get_image_url(instance)
        return representation


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
