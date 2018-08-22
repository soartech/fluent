from recommenderserver.recommender.row_strategies import *

class RowStrategyConfig(object):
    DEFAULT_COMPETENCY_ROW_STRATEGIES = [
        ReviewActivities,
        HighestRatedActivities,
        PopularActivities,
        AffectFrustratedOrBored,
        AffectBored,
        IntroductoryActivities,
        IntermediateActivities,
        ChallengingActivities,
        AffectConfusedOrNew,
        Shiny,
        NewCompetency,
        AllActivitiesForCompetency,
        MoveToNextSection
    ]

    PRIORITY_COMPETENCY_ROW_STRATEGIES = [
        AllActivitiesForCompetency,
        PopularActivities,
        HighestRatedActivities,
        FirstTimeNotAppropriateForExperts,
        MoreContentOrReferenceNotAppropriateForNovices,
        NewActivities,
        TimeForAnAssessment,
        TimeForCapstone,
        AffectConfusedOrNew,
        AffectFrustratedOrBored,
        AffectBored
    ]
    # Add for upcoming just AllActivities

    UPCOMING_COMPETENCY_ROW_STRATEGIES = [
        AllActivitiesForCompetency
    ]

    ELO_ROW_STRATEGIES_NO_MOODS = [
        ReviewActivities,
        PopularActivities,
        HighestRatedActivities,
        ChallengingActivities,
        IntermediateActivities,
        IntroductoryActivities,
        NewCompetency,
        Shiny,
        AllActivitiesForCompetency,
        MoveToNextSection
    ]

    PRIORITY_ACTIVITY_ROW_STRATEGIES = [
        MoreFromProviderActivities,
        MoreVideosActivities
    ]

    DEFAULT_ACTIVITY_ROW_STRATEGIES = [
        TakeAgainActivities,
        MoreFromAuthorActivities,
        MoreFromProviderActivities,
        MoreVideosActivities,
        MoreFromPreviousTLOs
    ]

    ACTIVITY_ROW_STRATEGIES_NO_MOODS = [
        TakeAgainActivities,
        MoreFromAuthorActivities,
        MoreFromProviderActivities,
        MoreVideosActivities,
        MoreFromPreviousTLOs
    ]

    MIN_CONTENT_THRESHOLD = 5

    NOT_ENOUGH_CONTENT_ELO_ROW_STRATEGIES = [
        AllActivitiesForCompetency
    ]

    NOT_ENOUGH_CONTENT_ACTIVITY_ROW_STRATEGIES = [
        MoreFromPreviousTLOs
    ]

    FILTER_LOCKED_ACTIVITIES = True
    CHECK_FOR_TOO_FEW_ACTIVITIES = False


class MandatoryAssignmentMakerConfig(object):
    TLO_UNIT_ASSESSMENT = False
    SELF_REPORT = True
    FORMATIVE_ASSESSMENT = True
    METACOGNITIVE_PROMPT = True
    USE_MANDATORY_ASSIGNMENTS = False
