from ratings.models import Rating

conf = ["version_0001"]

def version_0001(statementlink):
    '''Super simple first algorithm: Get all raters, weight by rating of raters'''
    ratings = statementlink.get_ratings()
    # Create dict of ratings to weight
    ratings_to_weight = []
    for rating in ratings:
        raw_rater_score = rating.added_by.get_score()
        rater_score = float(raw_rater_score.score) if raw_rater_score.score else .5 # provide low default
        ratings_to_weight.append({'rating': float(rating.rating), 'rater_score': rater_score })
    # Get total weight, we can get the weights to add up to 1
    total_weight = sum([item['rater_score'] for item in ratings_to_weight])
    # Now weight ratings
    total_score = 0.0
    for weighted_rating in ratings_to_weight:
        weight = float(weighted_rating['rater_score'])/total_weight
        total_score += float(weighted_rating['rating'])* weight
    return total_score
