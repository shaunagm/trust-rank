import datetime
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from rest_framework import generics, viewsets, permissions
from trustrank.permissions import IsOwnerAndNewData
from statements.models import Statement, StatementLink
from statements.forms import LinkedStatementForm
from statements.serializers import StatementSerializer, StatementLinkSerializer

class StatementIndexView(generic.ListView):
    model = Statement
    template_name = "statements/statement_index.html"

class StatementView(generic.DetailView):
    model = Statement
    template_name = 'statements/statement.html'

class AddStatementView(generic.edit.CreateView):
    model = Statement
    template_name = "statements/add_statement_form.html"
    fields = ['content', 'link', 'claimant']

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.added_by = self.request.user.profile
        return super(AddStatementView, self).form_valid(form)

class AddLinkedStatementView(generic.edit.CreateView):
    model = Statement
    template_name = "statements/add_linked_statement_form.html"
    form_class = LinkedStatementForm

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        form_kws = super(AddLinkedStatementView, self).get_form_kwargs()
        form_kws["user"] = self.request.user
        form_kws["linked_statement_pk"] = self.kwargs['pk']
        return form_kws

class StatementViewSet(viewsets.ModelViewSet):
    """
    Statement viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerAndNewData)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user.profile, date_added=timezone.now())

class StatementLinkViewSet(viewsets.ModelViewSet):
    """
    StatementLink viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = StatementLink.objects.all()
    serializer_class = StatementLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerAndNewData)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user.profile, date_added=timezone.now())
