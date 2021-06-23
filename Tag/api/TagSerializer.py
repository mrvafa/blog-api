from rest_framework.serializers import ModelSerializer

from Tag.models import Tag


class TagAllSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'image', 'body', 'added_datetime', 'modify_datetime', 'slug',)
        read_only_fields = ('added_datetime', 'modify_datetime', 'slug')


class TagSingleSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'image', 'body', 'added_datetime', 'modify_datetime', 'slug', 'posts')
        read_only_fields = ('posts', 'added_datetime', 'modify_datetime', 'slug')
