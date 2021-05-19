from rest_framework.serializers import ModelSerializer

from Post.models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        if args and args[0] and args[0].image and not kwargs.get('data').get('image'):
            kwargs['data']['image'] = args[0].image
        if args and args[0] and args[0].title and not kwargs.get('data').get('title'):
            kwargs['data']['title'] = args[0].title
        if args and args[0] and args[0].body and not kwargs.get('data').get('body'):
            kwargs['data']['body'] = args[0].body
        super(UpdatePostSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        fields = '__all__'
