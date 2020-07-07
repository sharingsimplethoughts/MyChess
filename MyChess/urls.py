"""MyChess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import activate

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),  # email varification
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    #apps
    path('accounts/',include('accounts.api.urls',namespace='accounts')),
    path('subscription/',include('usubscription.api.urls',namespace='usubscription')),
    path('category/',include('category.api.urls',namespace='category')),
    path('articles/',include('articles.api.urls',namespace='articles')),
    path('game/',include('game.api.urls',namespace='game')),
    path('tournament/',include('tournament.api.urls',namespace='tournament')),
    path('lessons/',include('lessons.api.urls',namespace='lessons')),
    path('achievement/',include('achievement.api.urls',namespace='achievement')),
    path('puzzles/',include('puzzles.api.urls',namespace='puzzles')),
    #admin_panel
    path('admin_panel/',include('_admin_panel.aaccounts.urls',namespace="ap_accounts")),
    path('admin_panel/articles/',include('_admin_panel.aarticles.urls',namespace='ap_articles')),
    path('admin_panel/videos/',include('_admin_panel.avideos.urls',namespace='ap_videos')),
    path('admin_panel/tournament/',include('_admin_panel.atournament.urls',namespace='ap_tournament')),
    path('admin_panel/usermgmt/',include('_admin_panel.ausermgmt.urls',namespace='ap_usermgmt')),
    path('admin_panel/settings/',include('_admin_panel.asettings.urls',namespace='ap_settings')),
    path('admin_panel/notification/',include('_admin_panel.anotification.urls',namespace='ap_notification')),
    path('admin_panel/lessons/',include('_admin_panel.alessons.urls',namespace='ap_lessons')),
    path('admin_panel/gametime/',include('_admin_panel.agametime.urls',namespace='ap_gametime')),
    path('admin_panel/subscription/',include('_admin_panel.asubscription.urls',namespace='ap_subscription')),
    path('admin_panel/leaderboard/',include('_admin_panel.aleaderboard.urls',namespace='ap_leaderboard')),
    path('admin_panel/achievement/',include('_admin_panel.aachievement.urls',namespace='ap_achievement')),
    path('admin_panel/payment/',include('_admin_panel.apayment.urls',namespace='ap_payment')),
    path('admin_panel/puzzles/',include('_admin_panel.apuzzles.urls',namespace='ap_puzzles')),
]
# urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)