from django.db.models import Avg
from rest_framework import serializers

from main.models import Airplane, Person, Ticket, Country, Comment, Likes, Rating, Favorite


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
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        representation['image'] = self._get_image_url(instance)
        return representation


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(author=request.user,
                                     **validated_data)
        return comment


class LikesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        ticket = validated_data.get('ticket')
        like = Likes.objects.get_or_create(author=author, ticket=ticket)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        ticket = validated_data.get('ticket')
        rating = Rating.objects.get_or_create(author=author, ticket=ticket)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['ticket'] = instance.ticket.name
        return representation