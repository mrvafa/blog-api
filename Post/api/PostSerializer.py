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
    author = serializers.ReadOnlyField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'slug', 'added_datetime', 'modify_datetime', 'author')

    def update(self, instance, validated_data):
        if 'tags' not in validated_data:
            instance.tags.clear()
        return super(UpdatePostSerializer, self).update(instance, validated_data)


class CreatePostSerializer(serializers.ModelSerializer):
    added_datetime = serializers.DateTimeField(read_only=True)
    modify_datetime = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'slug', 'added_datetime', 'modify_datetime', 'author')

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super(CreatePostSerializer, self).create(validated_data)
