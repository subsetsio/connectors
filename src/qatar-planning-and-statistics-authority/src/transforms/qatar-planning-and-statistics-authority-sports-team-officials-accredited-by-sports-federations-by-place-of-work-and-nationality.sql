-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "teams_qataris",
    "teams_non_qataris",
    "teams_total",
    "clubs_qataris",
    "clubs_non_qataris",
    "clubs_total",
    "total_qataris",
    "total_non_qataris",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-sports-team-officials-accredited-by-sports-federations-by-place-of-work-and-nationality"
