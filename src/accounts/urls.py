from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^$', views.ProfileIndexView.as_view(), name='profile_index'),
    url(r'^p/add$', views.AddClaimantView.as_view(), name='add_claimant'),
    url(r'^p/(?P<pk>[-\w]+)$', views.ProfileView.as_view(), name='profile'),
]
