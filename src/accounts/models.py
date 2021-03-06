from __future__ import unicode_literals

import datetime, random, string

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from trustrank.settings import PRODUCTION_DOMAIN, NOTIFY_EMAIL

class ProfileQuerySet(models.QuerySet):

    def members(self):
        return self.filter(member=True)

    def vetted_members(self):
        return self.filter(vetted_member=True)

    def claimants(self):
        return self.filter(claimant=True)

class Profile(models.Model):
    '''Account info.  Profile may be a user of the site, a claimant (account to whom
    statements are attributed), or both.'''
    user = models.OneToOneField(User, unique=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    # Membership info
    member = models.BooleanField(default=False)
    date_joined = models.DateTimeField(blank=True, null=True)
    # Claimant info
    claimant = models.BooleanField(default=False)
    claimant_name = models.CharField(max_length=50, blank=True, null=True)
    claimant_bio = models.CharField(max_length=500, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    added_by = models.ForeignKey("self", null=True, related_name="created_claimants")
    # Vetting info
    vetted_member = models.BooleanField(default=False)
    date_vetted = models.DateTimeField(blank=True, null=True)

    scores = GenericRelation("ratings.score")

    objects = ProfileQuerySet.as_manager() # Custom manager

    def __unicode__(self):
        if self.user and self.claimant:
            return "%s (User & Claimant)" % self.user.username
        if self.user:
            return "%s (User)" % self.user.username
        if self.claimant:
            return "%s (Claimant)" % self.claimant_name

    def name(self):
        if self.user and self.claimant:
            return "%s" % self.user.username
        if self.user:
            return "%s" % self.user.username
        if self.claimant:
            return "%s" % self.claimant_name

    def class_name(self):
        return "profile"

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk':self.pk})

    def get_ratings(self):
        from ratings.models import Rating
        ct = ContentType.objects.get(app_label="accounts", model="profile")
        return Rating.objects.filter(content_type=ct, object_id=self.pk)

    def ratings_made(self):
        from ratings.models import Rating
        return Rating.objects.filter(added_by=self)

    def get_score(self, score_type="user_trust"):
        from ratings.models import Score
        ct = ContentType.objects.get(app_label="accounts", model="profile")
        score, created = Score.objects.get_or_create(content_type=ct, object_id=self.pk,
            score_type=score_type)
        return score

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        slug = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))
        ar = ActiveRegistration.objects.create(user=instance, confirmation_slug=slug)
        # Send confirmation email
        from django.core.mail import send_mail
        woo = instance.username
        message = "Hello %s!  To confirm your account, please follow this link: <a href='%s'>%s</a>" % (woo, ar.confirmation_link(), ar.confirmation_link())
        send_mail('Confirm your account on TrustRank', message, NOTIFY_EMAIL,
            [ar.user.email], html_message=message, fail_silently=False)
post_save.connect(create_user_profile, sender=User)

class ActiveRegistration(models.Model):
    '''Data table for storing temporary information about accounts'''
    user = models.OneToOneField(User, unique=True, null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    confirmation_slug = models.CharField(max_length=30, blank=True)
    confirmed = models.BooleanField(default=False)

    def confirmation_link(self):
        return PRODUCTION_DOMAIN + reverse('sign_up_confirmation', kwargs={'slug': self.confirmation_slug })
