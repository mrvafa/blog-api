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
