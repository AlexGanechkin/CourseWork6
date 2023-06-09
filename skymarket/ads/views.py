from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsCurrentUser, IsAdmin
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter
    serializer_class = AdSerializer

    def get_queryset(self):
        if self.action == 'me':
            return Ad.objects.filter(author=self.request.user).all()
        return Ad.objects.all()

    def get_permissions(self):
        if self.action in ['list']:
            self.permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'create', 'me']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['partial_update', 'destroy']:
            self.permission_classes = [IsCurrentUser]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'partial_update']:
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])
        return ad_instance.comment_set.all()

    #def get_permissions(self):
    #    if self.action in ['list', 'create']:
    #        self.permission_classes = [IsAuthenticated, IsAdminUser]
    #    elif self.action in ['partial_update', 'update', 'destroy']:
    #        self.permission_classes = [IsAuthenticated, IsCurrentUser, IsAdminUser]
    #    else:
    #        self.permission_classes = [IsAuthenticated, IsAdminUser]
    #    return super().get_permissions()

   #def get_permissions(self):
   #    if self.action == "retrieve":
   #        self.permission_classes = [IsAuthenticated, ]
   #    elif self.action in ["create", "update", "partial_update", "destroy", ]:
   #        self.permission_classes = [IsAuthenticated, IsAdmin | IsCurrentUser]
   #    return super().get_permissions()

    def perform_create(self, serializer):
        ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])
        user = self.request.user
        serializer.save(author=user, ad=ad_instance)
