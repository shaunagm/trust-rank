from django import forms
from django.forms import ChoiceField, Select
from django.forms.widgets import HiddenInput

from statements.models import Statement, StatementLink, STATEMENT_LINK_CHOICES

class LinkedStatementForm(forms.ModelForm):
    kind = ChoiceField(label='Kind of link', widget=Select(), choices=STATEMENT_LINK_CHOICES,
        required=True)

    class Meta:
        model = Statement
        fields = ['content', 'link', 'claimant']

    def __init__(self, user, linked_statement_pk, *args, **kwargs):
        super(LinkedStatementForm, self).__init__(*args, **kwargs)
        self.user = user
        self.linked_statement = Statement.objects.get(pk=linked_statement_pk)

    def save(self, commit=True):
        instance = super(LinkedStatementForm, self).save(commit=False)
        instance.added_by = self.user.profile
        instance.save()
        # Create link
        link_kind = self.cleaned_data['kind']
        StatementLink.objects.create(parent=self.linked_statement, child=instance,
            kind=link_kind, added_by=self.user.profile)
        return instance
