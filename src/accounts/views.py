from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets, permissions

from trustrank.permissions import IsOwnerAndNewData
from accounts.models import Profile, ActiveRegistration
from accounts.serializers import ProfileSerializer
from accounts.forms import SignUpForm

class ProfileIndexView(generic.ListView):
    model = Profile
    template_name = "accounts/profile_index.html"

class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

class AddClaimantView(LoginRequiredMixin, generic.edit.CreateView):
    model = Profile
    template_name = "accounts/add_claimant_form.html"
    fields = ['claimant_name', 'claimant_bio']

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.claimant = True
        form.instance.added_by = self.request.user.profile
        return super(AddClaimantView, self).form_valid(form)

##################################
### Registration-related views ###
##################################

class SignUpView(generic.edit.CreateView):
    model = Profile
    form_class = SignUpForm
    template_name = "accounts/authentication_and_registration/signup_form.html"

    def get_success_url(self, **kwargs):
        return reverse('sent_confirmation')

def signup_confirmation_view(request, slug):
    try:
        ar = ActiveRegistration.objects.get(confirmation_slug=slug)
        if ar.confirmed == True:
            return HttpResponseRedirect(reverse('already_registered'))
        else:
            user = ar.user
            user.is_active = True
            user.save()
            profile = Profile.objects.create(user=user)
            profile.member = True
            profile.date_joined = timezone.now()
            profile.save()
            ar.confirmed = True
            ar.save()
    except:
        return HttpResponseRedirect(reverse('generic_problem'))
    return render(request, 'accounts/authentication_and_registration/signup_confirmation.html')

class GenericProblemView(generic.TemplateView):
    template_name = "accounts/authentication_and_registration/generic_problem.html"

class AlreadyRegisteredView(generic.TemplateView):
    template_name = "accounts/authentication_and_registration/already_registered.html"

class SentView(generic.TemplateView):
    template_name = "accounts/authentication_and_registration/confirmation_sent.html"

#################
### API views ###
#################

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
