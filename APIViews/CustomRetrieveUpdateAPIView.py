from django.forms import model_to_dict
from rest_framework.generics import RetrieveUpdateAPIView


class RetrieveUpdateBlankUseDefaultAPIView(RetrieveUpdateAPIView):
    """
    If the value passed None, use previous data that is in DB.
    """

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        for field in model_to_dict(instance):
            if field not in request.data:
                request.data[field] = model_to_dict(instance)[field]
        return super(RetrieveUpdateBlankUseDefaultAPIView, self).put(request, args, kwargs)
