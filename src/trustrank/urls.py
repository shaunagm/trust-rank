"""trustrank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView

# Handles API urls
from rest_framework import routers, schemas
schema_view = schemas.get_schema_view(title='TrustRank API')
from accounts.views import ProfileViewSet
from ratings.views import RatingViewSet
from statements.views import StatementViewSet, StatementLinkViewSet
router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'statements', StatementViewSet)
router.register(r'statementlinks', StatementLinkViewSet)

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='about', permanent=False)),
    url(r'^about/$', TemplateView.as_view(template_name='trustrank/about.html'), name='about'),
    url(r'^admin/', admin.site.urls),
    # App urls
    url(r'^accounts/', include('accounts.urls')),
    url(r'^statements/', include('statements.urls')),
    url(r'^ratings/', include('ratings.urls')),
    ## Auth urls
    url(r'^login/$', auth_views.login, {'template_name': 'accounts/authentication_and_registration/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    # API urls
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/schema/$', schema_view),
]
