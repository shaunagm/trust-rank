from rest_framework import serializers
from accounts.models import Profile
from statements.models import Statement

from ratings.serializers import ScoreSerializer

class ProfileSerializer(serializers.ModelSerializer):
    '''Note that the profile serializer is used only for creating claimants, not users'''
    # Read only related fields
    statements_added = serializers.HyperlinkedRelatedField(many=True, read_only=True,
        view_name='api:statement-detail')
    added_by = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api:profile-detail')
    scores = ScoreSerializer(read_only=True, many=True)

    # Read only fields (user/membership data)
    member = serializers.ReadOnlyField()
    date_joined = serializers.ReadOnlyField()
    bio = serializers.ReadOnlyField()
    claimant = serializers.ReadOnlyField()
    date_added = serializers.ReadOnlyField()
    vetted_member = serializers.ReadOnlyField()
    date_vetted = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('id', 'member', 'date_joined', 'bio', 'claimant', 'date_added',
            'claimant_name', 'claimant_bio', 'added_by', 'vetted_member', 'date_vetted',
            'statements_added', 'scores')
