from rest_framework import serializers

from Post.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', )
    tags = serializers.StringRelatedField(many=True, read_only=True, )
    added_datetime = serializers.DateTimeField(read_only=True)
    modify_datetime = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'image', 'body', 'added_datetime', 'modify_datetime', 'tags', 'author')


class UpdatePostSerializer(serializers.ModelSerializer):
    added_datetime = serializers.DateTimeField(read_only=True)
    modify_datetime = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'slug', 'added_datetime', 'modify_datetime',)


class CreatePostSerializer(serializers.ModelSerializer):
    added_datetime = serializers.DateTimeField(read_only=True)
    modify_datetime = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'slug', 'added_datetime', 'modify_datetime',)

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super(CreatePostSerializer, self).create(validated_data)
