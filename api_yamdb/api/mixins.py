from rest_framework import mixins, viewsets


class ModelMixins(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для наследования"""
    pass
