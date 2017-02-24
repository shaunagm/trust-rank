from django.core.management.base import BaseCommand, CommandError

from accounts.models import Profile
from statements.models import Statement, StatementLink

class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            # User trust
            for p in Profile.objects.all():
                score = p.get_score()
                score.calculate_score()
            print("User trust scores calculated")
            # Statement trust and statement verification
            for s in Statement.objects.all():
                score = s.get_score()
                score.calculate_score()
                verification_score = s.get_score("underverified")
                verification_score.calculate_score()
            print("Statement scores calculated")
            # Statementlink trust score
            for sl in StatementLink.objects.all():
                score = sl.get_score()
                score.calculate_score()
            print("Statementlink trust scores calculated")
        except:
            raise CommandError("Failure calculating scores")
