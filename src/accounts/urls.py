from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^$', views.ProfileIndexView.as_view(), name='profile_index'),
    url(r'^p/add$', views.AddClaimantView.as_view(), name='add_claimant'),
    url(r'^p/(?P<pk>[-\w]+)$', views.ProfileView.as_view(), name='profile'),
    # Registration
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^sent/$', views.SentView.as_view(), name='sent_confirmation'),
    url(r'^sign-up-confirmation/(?P<slug>[-\w]+)/$', views.signup_confirmation_view, name='sign_up_confirmation'),
    url(r'^generic_problem/$', views.GenericProblemView.as_view(), name='generic_problem'),
    url(r'^already_registered/$', views.AlreadyRegisteredView.as_view(), name='already_registered'),
]
