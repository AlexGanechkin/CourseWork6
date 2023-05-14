from django.urls import include, path
from rest_framework_nested import routers

from ads.views import AdViewSet, CommentViewSet

ad_router = routers.SimpleRouter()
ad_router.register('ads', AdViewSet, basename='ads')
comments_router = routers.NestedSimpleRouter(ad_router, r'ads', lookup='ad')
comments_router.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(ad_router.urls)),
    path('', include(comments_router.urls))
]
