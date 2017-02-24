import inspect, pprint
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required

from rest_framework import generics, viewsets, permissions
from trustrank.permissions import IsOwnerAndNewData
from ratings.models import Rating
from ratings.serializers import RatingSerializer

@login_required
def add_rating(request):

    try:
        user = request.user.profile # check for authentication
        rating = request.POST.get('rating', None)

        model = request.POST.get('model', None)
        pk = request.POST.get('pk', None)

        if model.lower() in ["statement", "statementlink"]:
            app_label = "statements"
        if model.lower() in ["profile"]:
            app_label = "accounts"
        ct = ContentType.objects.get(app_label=app_label, model=model.lower())
        rated_object =  ct.get_object_for_this_type(pk=int(pk)) # Check that it exists!

        Rating.objects.create(content_type=ct, object_id=int(pk), added_by=user, rating=rating)

        data = { 'status': 'success', 'success': True }

    except:

        data = { 'status': 'failed' }

    return JsonResponse(data)

class RatingViewSet(viewsets.ModelViewSet):
    """
    Rating viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerAndNewData)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user.profile, date_added=timezone.now())

class AlgorithmInpsectView(generic.TemplateView):
    template_name="ratings/display_algorithms.html"

    def get_context_data(self, **kwargs):
        context = super(AlgorithmInpsectView, self).get_context_data(**kwargs)
        from ratings.lib.algorithms import usertrust
        trust_string = inspect.getsource(usertrust)
        context['usertrust'] = highlight(trust_string, PythonLexer(), HtmlFormatter())
        from ratings.lib.algorithms import statementtrust
        trust_string = inspect.getsource(statementtrust)
        context['statementtrust'] = highlight(trust_string, PythonLexer(), HtmlFormatter())
        from ratings.lib.algorithms import statementlinktrust
        trust_string = inspect.getsource(statementlinktrust)
        context['statementlinktrust'] = highlight(trust_string, PythonLexer(), HtmlFormatter())
        from ratings.lib.algorithms import underverified
        trust_string = inspect.getsource(underverified)
        context['underverified'] = highlight(trust_string, PythonLexer(), HtmlFormatter())
        return context
