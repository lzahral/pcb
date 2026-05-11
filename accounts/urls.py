from django.urls import include, path
from .views import *

urlpatterns = [
    # user
    # path('', UsersListView.as_view(), name='user_list'),
    # path('create/', UserCreateView.as_view(), name='user_create'),
    # path("edit/<int:pk>/", UserUpdateView.as_view(), name="user_edit"),
    # path("edit/profile/", ProfileUpdateView.as_view(), name="profile_edit"),
    # path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),

    # authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]
