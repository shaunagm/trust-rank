from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from statements import views

urlpatterns = [
    url(r'^$', views.StatementIndexView.as_view(), name='statement_index'),
    url(r'^s/add$', views.AddStatementView.as_view(), name='add_statement'),
    url(r'^s/(?P<pk>[-\w]+)$', views.StatementView.as_view(), name='statement'),
    url(r'^s/(?P<pk>[-\w]+)/add$', views.AddLinkedStatementView.as_view(), name='add_linked_statement'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
