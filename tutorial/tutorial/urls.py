from django.urls import include, path
from django.contrib import admin
from rest_framework_extensions.routers import ExtendedDefaultRouter

from quickstart.router import SwitchDetailRouter
from quickstart.views import \
    UserViewSet, TweetViewSet, \
    UserTweetsViewSet, FollowViewSet, \
    FeedViewSet, FollowsViewSet, FollowerViewSet

# switch_router = SwitchDetailRouter()
#
# router = ExtendedDefaultRouter()
# router.register(r'users', UserViewSet).register(
#     'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
# router.register(r'tweets', TweetViewSet)
# router.register(r'feed', FeedViewSet)
# switch_router.register(r'follow', FollowViewSet)

switch_router = SwitchDetailRouter()

router = ExtendedDefaultRouter()
user = router.register(r'users', UserViewSet)
user.register(r'tweets', UserTweetsViewSet, 'user-tweets', ['username'])
user.register(r'follows', FollowsViewSet, 'user-follows', ['username'])
user.register(r'followed', FollowerViewSet, 'user-follower', ['username'])
switch_router.register(r'follow', FollowViewSet)
router.register(r'tweets', TweetViewSet)
router.register(r'feed', FeedViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/', include(switch_router.urls)),
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]