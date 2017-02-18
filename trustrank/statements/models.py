from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from accounts.models import Profile

class Statement(models.Model):
    content = models.CharField(max_length=5000, blank=True, null=True)
    link = models.CharField(max_length=500)
    added_by = models.ForeignKey(Profile, related_name="statements_added")
    claimant = models.ForeignKey(Profile, related_name="claims")
    date_added = models.DateTimeField(default=timezone.now)
    linked_statements = models.ManyToManyField('self', through='StatementLink',
        symmetrical=False, related_name='linked_to')
    scores = GenericRelation("ratings.score")

    def __unicode__(self):
        return "%s (claimed by %s)" % (self.name(), self.claimant.name())

    def name(self):
        if self.content:
            if len(self.content) > 50:
                slug = self.content[:50]
            else:
                slug = self.content
        else:
            slug = self.link
        return slug

    def class_name(self):
        return "statement"

    def get_absolute_url(self):
        return reverse('statement', kwargs={'pk':self.pk})

    def get_ratings(self):
        from ratings.models import Rating
        ct = ContentType.objects.get(app_label="statements", model="statement")
        return Rating.objects.filter(content_type=ct, object_id=self.pk)

    def get_score(self, score_type="statement_trust"):
        from ratings.models import Score
        ct = ContentType.objects.get(app_label="statements", model="statement")
        score, created = Score.objects.get_or_create(content_type=ct, object_id=self.pk,
            score_type=score_type)
        return score

    def get_verifications(self):
        links = StatementLink.objects.filter(parent=self)
        return [sl.child for sl in links if sl.kind == "verifies"]

    def get_statement_links(self):
        return StatementLink.objects.filter(models.Q(parent=self) | models.Q(child=self))

STATEMENT_LINK_CHOICES = (
    ('contains', _('is contained by')),  # Child is contained by parent
    ('attributes', _('provides attribution for')),  # Child provides attribution for parent
    ('verifies', _('verifies')),  # Child verifies parent
    )

class StatementLink(models.Model):
    parent = models.ForeignKey(Statement, related_name='children')
    child = models.ForeignKey(Statement, related_name='parents')
    kind = models.CharField(max_length=15, choices=STATEMENT_LINK_CHOICES, default='verifies')
    added_by = models.ForeignKey(Profile, related_name="statementlinks_added")
    date_added = models.DateTimeField(default=timezone.now)
    scores = GenericRelation("ratings.score")

    def __unicode__(self):
        return "%s %s %s" % (self.child, self.kind, self.parent)

    def class_name(self):
        return "statementlink"

    def name_and_date(self):
        return "%s %s %s (Added %s by %s)" % (self.child, self.kind, self.parent,
            self.child.date_added, self.child.added_by)

    def get_ratings(self):
        from ratings.models import Rating
        ct = ContentType.objects.get(app_label="statements", model="statementlink")
        return Rating.objects.filter(content_type=ct, object_id=self.pk)

    def get_score(self, score_type="statementlink_trust"):
        from ratings.models import Score
        ct = ContentType.objects.get(app_label="statements", model="statementlink")
        score, created = Score.objects.get_or_create(content_type=ct, object_id=self.pk,
            score_type=score_type)
        return score

    def describe_given_object_relationship_to_parent(self):
        '''Describing given child's relationship to parent, i.e. object verifies parent'''
        return "%s <a href='%s'>%s</a>" % (self.get_kind_display(), self.parent.get_absolute_url(),
            self.parent)

    def describe_given_object_relationship_to_child(self):
        '''Describing given parent's relationship to child, i.e. object is verified by child'''
        # self.kind is written as child-to-parent by default, so we need to provide wording for the
        # reverse
        phrasing_dict = { 'contains': 'contains', 'attributes': 'is attributed by',
            'verifies': 'is verified by'}
        return "%s <a href='%s'>%s</a>" % (phrasing_dict[self.kind], self.child.get_absolute_url(),
            self.child)
