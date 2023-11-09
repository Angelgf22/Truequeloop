"""
URL configuration for truequeloop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.truequeloop_app.views import (
    home_screen_view, community_screen_view, login_screen_view, register_screen_view, create_trade_screen_view,
    trade_screen_view, logout_user, chat_view, profile_view, delete_trade, delete_account, edit_profile, edit_trade,
    community_request_screen_view, open_chats_screen_view, moderator_panel_screen_view, create_community_screen_view,
    manage_communities_screen_view, delete_community, edit_community, delete_request, delete_trade_staff
)

urlpatterns = [
            path('', home_screen_view, name="home"),
            path('admin/', admin.site.urls),
            path('community/<int:id>', community_screen_view, name="community"),
            path('login/', login_screen_view, name="login"),
            path('logout/', logout_user, name="logout"),
            path('register/', register_screen_view, name="register"),
            path('create-trade/', create_trade_screen_view, name="createTrade"),
            path('trade/<int:id>', trade_screen_view, name="trade"),
            path('chat/<str:username>/', chat_view, name='chat'),
            path('profile', profile_view, name='profile'),
            path('delete-trade/<int:trade_id>', delete_trade, name='delete-trade'),
            path('delete-account/<int:user_id>', delete_account, name='delete-account'),
            path('edit-profile', edit_profile, name='edit-profile'),
            path('edit-trade/<int:trade_id>', edit_trade, name='edit-trade'),
            path('community-request', community_request_screen_view, name='community-request'),
            path('messages/', open_chats_screen_view, name='open-chats'),
            path('moderator-panel/', moderator_panel_screen_view, name='moderation'),
            path('create-community/', create_community_screen_view, name='create-community'),
            path('manage-communities/', manage_communities_screen_view, name='manage-communities'),
            path('delete-community/<int:community_id>', delete_community, name='delete-community'),
            path('edit-community/<int:community_id>', edit_community, name='edit-community'),
            path('delete-request/<int:request_id>', delete_request, name='delete-request'),
            path('delete-trade-staff/<int:trade_id>', delete_trade_staff, name='delete-trade-staff'),


              ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
