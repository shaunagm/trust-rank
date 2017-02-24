from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from rest_framework import generics, viewsets, permissions
from trustrank.permissions import IsOwnerAndNewData
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class ProfileIndexView(generic.ListView):
    model = Profile
    template_name = "accounts/profile_index.html"

class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

class AddClaimantView(generic.edit.CreateView):
    model = Profile
    template_name = "accounts/add_claimant_form.html"
    fields = ['claimant_name', 'claimant_bio']

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.claimant = True
        form.instance.added_by = self.request.user
        return super(AddClaimantView, self).form_valid(form)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    Profile viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerAndNewData)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user.profile, date_added=timezone.now(),
            claimant=True)
