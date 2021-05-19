from rest_framework import serializers

from Post.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', )
    tags = serializers.StringRelatedField(many=True, read_only=True, )

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'image', 'body', 'added_datetime', 'modify_datetime', 'tags',
                  'author')


class UpdatePostSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        if kwargs and 'data' in kwargs and kwargs['data']:
            # remember old state
            _mutable = kwargs['data']._mutable
            # set to mutable
            kwargs['data']._mutable = True

            if args and args[0] and args[0].image and not kwargs.get('data').get('image'):
                kwargs['data']['image'] = args[0].image
            if args and args[0] and args[0].title and not kwargs.get('data').get('title'):
                kwargs['data']['title'] = args[0].title
            if args and args[0] and args[0].body and not kwargs.get('data').get('body'):
                kwargs['data']['body'] = args[0].body

            kwargs['data']._mutable = _mutable
        super(UpdatePostSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags')


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super(CreatePostSerializer, self).create(validated_data)
