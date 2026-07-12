-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "teams_qatari",
    "teams_non_qatari",
    "teams_total",
    "clubs_qatari",
    "clubs_non_qatari",
    "clubs_total",
    "total_qatari",
    "total_non_qatari",
    "total_overall"
FROM "qatar-planning-and-statistics-authority-assassistant-coaches-accredited-in-sports-federations-by-sports-activity-place-of-work-and"
