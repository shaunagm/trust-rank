from statements.models import Statement

conf = ["version_0001"]

def version_0001(statement):
    '''Super simple first algorithm: calculate ratio of verifications to ratings '''
    ratings = statement.get_ratings()
    verifications = statement.get_verifications()
    if len(ratings) == 0:  # A statement with no ratings needs no verifications
        return 0
    else:
        ratings_count = 1.0 + len(ratings)
        verifications_count = 1.0 + len(verifications)
        return ratings_count/verifications_count
