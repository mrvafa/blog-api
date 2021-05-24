from django.forms import model_to_dict
from rest_framework.generics import RetrieveUpdateAPIView


class RetrieveUpdateBlankUseDefaultAPIView(RetrieveUpdateAPIView):
    """
    If the value passed None, use previous data that is in DB.
    """

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        _mutable = None
        if '_mutable' in dir(request.data):
            _mutable = request.data._mutable
            request.data._mutable = True
        for field in model_to_dict(instance):
            if field not in request.data:
                if model_to_dict(instance)[field]:
                    request.data[field] = model_to_dict(instance)[field]
        if '_mutable' in dir(request.data):
            request.data._mutable = _mutable
        return super(RetrieveUpdateBlankUseDefaultAPIView, self).put(request, args, kwargs)
