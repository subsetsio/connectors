-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide student engagement table; columns encode engagement and badges by income segment and school-break status, so compare like-named measures rather than summing across all engagement and badges columns.
SELECT
    "year",
    "month",
    "day_endofweek",
    "engagement",
    "badges",
    "engagement_inchigh",
    "badges_inchigh",
    "engagement_inclow",
    "badges_inclow",
    "engagement_incmiddle",
    "badges_incmiddle",
    "break_engagement",
    "break_badges",
    "break_engagement_inchigh",
    "break_badges_inchigh",
    "break_engagement_inclow",
    "break_badges_inclow",
    "break_engagement_incmiddle",
    "break_badges_incmiddle"
FROM "opportunity-insights-tracker-zearn-national-weekly"
