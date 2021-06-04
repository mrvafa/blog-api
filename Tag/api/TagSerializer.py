from rest_framework.serializers import ModelSerializer

from Tag.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'image', 'body', 'added_datetime', 'modify_datetime', 'slug')


class UpdateTagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title', 'image', 'body')


class RemoveTagImageSerializer(UpdateTagSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data.pop('image')
        instance.image = None
        return super().update(instance, validated_data)
