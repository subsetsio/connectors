-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "teams_associations_qataris",
    "teams_associations_non_qataris",
    "clubs_qataris",
    "clubs_non_qataris"
FROM "qatar-planning-and-statistics-authority-physiotherapists-accredited-in-sports-federations-by-sports-activity-place-of-work-and-nationality"
