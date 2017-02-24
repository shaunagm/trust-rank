from django.utils import timezone
from rest_framework import serializers
from accounts.models import Profile
from statements.models import Statement, StatementLink
from ratings.serializers import ScoreSerializer

class StatementLinkSerializer(serializers.ModelSerializer):
    added_by = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api:profile-detail')
    date_added = serializers.ReadOnlyField()
    parent = serializers.HyperlinkedRelatedField(many=False, queryset=Statement.objects.all(),
        view_name='api:statement-detail')
    child = serializers.HyperlinkedRelatedField(many=False, queryset=Statement.objects.all(),
        view_name='api:statement-detail')
    scores = ScoreSerializer(read_only=True, many=True)

    class Meta:
        model = StatementLink
        fields = ('id', 'parent', 'child', 'kind', 'added_by', 'date_added', 'scores')

    def validate(self, data):
        """
        Check that the child is not the same as the parent
        """
        if data['parent'] == data['child']:
            raise serializers.ValidationError("Parent and child must be different statements")
        return data

class StatementSerializer(serializers.ModelSerializer):
    added_by = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api:profile-detail')
    date_added = serializers.ReadOnlyField()
    claimant = serializers.HyperlinkedRelatedField(many=False, queryset=Profile.objects.claimants(),
        view_name='api:profile-detail')
    parents = StatementLinkSerializer(many=True, read_only=True)
    children = StatementLinkSerializer(many=True, read_only=True)
    scores = ScoreSerializer(read_only=True, many=True)

    class Meta:
        model = Statement
        fields = ('id', 'content', 'link', 'date_added', 'added_by', 'claimant',
            'parents', 'children', 'scores')
