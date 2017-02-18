from django.utils import timezone

from rest_framework import serializers
from generic_relations.relations import GenericRelatedField

from ratings.models import Rating, Score
from accounts.models import Profile
from statements.models import Statement, StatementLink

class RatingSerializer(serializers.ModelSerializer):
    added_by = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api:profile-detail')
    rated_object = GenericRelatedField({
        Statement: serializers.HyperlinkedRelatedField(
            queryset = Statement.objects.all(),
            view_name='api:statement-detail',
        ),
        StatementLink: serializers.HyperlinkedRelatedField(
            queryset = StatementLink.objects.all(),
            view_name='api:statementlink-detail',
        ),
        Profile: serializers.HyperlinkedRelatedField(
            queryset = Profile.objects.all(),
            view_name='api:profile-detail',
        ),
    })
    date_added = serializers.ReadOnlyField()

    class Meta:
        model = Rating
        fields = ('rated_object', 'rating', 'rating_type', 'added_by', 'date_added')

class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ('score', 'score_type', 'algorithm_version', 'last_calculated')
