from rest_framework.serializers import ModelSerializer

from Tag.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UpdateTagSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        if args and args[0] and args[0].image and not kwargs.get('data').get('image'):
            kwargs['data']['image'] = args[0].image
        if args and args[0] and args[0].title and not kwargs.get('data').get('title'):
            kwargs['data']['title'] = args[0].title
        if args and args[0] and args[0].body and not kwargs.get('data').get('body'):
            kwargs['data']['body'] = args[0].body
        super(UpdateTagSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Tag
        fields = '__all__'


class RemoveTagImageSerializer(UpdateTagSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data.pop('image')
        instance.image = None
        return super().update(instance, validated_data)
