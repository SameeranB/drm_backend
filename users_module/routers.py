from rest_framework import routers

from users_module.views import UserViewSet

UserRouter = routers.DefaultRouter(trailing_slash=False)

UserRouter.register('users', UserViewSet, basename='user')
