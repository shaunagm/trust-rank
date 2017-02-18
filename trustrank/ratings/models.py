from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import Profile

class RatingQuerySet(models.QuerySet):

    def statements(self):
        ct = ContentType.objects.get(app_label="statements", model="statement")
        return self.filter(content_type=ct)

    def statementlinks(self):
        ct = ContentType.objects.get(app_label="statements", model="statementlink")
        return self.filter(content_type=ct)

    def profiles(self):
        ct = ContentType.objects.get(app_label="accounts", model="profile")
        return self.filter(content_type=ct)

    def accurate(self):
        return self.filter(rating_type="accuracy")

    def precise(self):
        return self.filter(rating_type="precision")

RATING_CHOICES = (
    ('accuracy', _('Accuracy')),
    ('precision', _('Precision')),
    )

class Rating(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    rated_object = GenericForeignKey('content_type', 'object_id')
    added_by = models.ForeignKey(Profile, related_name="ratings")
    date_added = models.DateTimeField(default=timezone.now)
    rating_type = models.CharField(max_length=15, choices=RATING_CHOICES, default='accuracy')
    rating = models.IntegerField(default=0)

    objects = RatingQuerySet.as_manager() # Custom manager

    def __unicode__(self):
        return "%s rated %s by %s" % (self.rated_object, self.rating, self.added_by)

SCORE_CHOICES = (
    ('undefined', _('Undefined')),
    ('user_trust', _('User Trust Score')),
    ('statement_trust', _('Statement Trust Score')),
    ('statementlink_trust', _('StatementLink Trust Score')),
    ('underverified', _('Unververified Statements Score')),
)

class Score(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    scored_object = GenericForeignKey('content_type', 'object_id')
    score = models.CharField(max_length=15, blank=True, null=True)
    score_type = models.CharField(max_length=20, choices=SCORE_CHOICES, default='undefined')
    algorithm_version = models.CharField(max_length=20, blank=True, null=True)
    last_calculated = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "Score %s for %s (type: %s, last calculated %s)" % (self.score, self.scored_object,
            self.score_type, self.last_calculated)

    def calculate_score(self):
        algorithm = self.get_algorithm()
        self.score = algorithm(self.scored_object)
        if algorithm != self.algorithm_version:  # TODO: save algorithm version name, not method itself
            self.algorithm_version = algorithm
        self.last_calculated = timezone.now()
        self.save()
        return self.score

    def get_algorithm(self):
        if self.score_type == "user_trust":
            from ratings.lib.algorithms import usertrust
            latest_alg = usertrust.conf[-1]
            return getattr(usertrust, latest_alg)
        if self.score_type == "statement_trust":
            from ratings.lib.algorithms import statementtrust
            latest_alg = statementtrust.conf[-1]
            return getattr(statementtrust, latest_alg)
        if self.score_type == "statementlink_trust":
            from ratings.lib.algorithms import statementlinktrust
            latest_alg = statementlinktrust.conf[-1]
            return getattr(statementlinktrust, latest_alg)
        if self.score_type == "underverified":
            from ratings.lib.algorithms import underverified
            latest_alg = underverified.conf[-1]
            return getattr(underverified, latest_alg)
