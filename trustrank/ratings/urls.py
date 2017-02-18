from django.conf.urls import url

from ratings import views

urlpatterns = [
    url(r'^add-rating/$', views.add_rating, name='add_rating'),
    url(r'^algorithms/$', views.AlgorithmInpsectView.as_view(), name='inspect_algorithms'),
]
