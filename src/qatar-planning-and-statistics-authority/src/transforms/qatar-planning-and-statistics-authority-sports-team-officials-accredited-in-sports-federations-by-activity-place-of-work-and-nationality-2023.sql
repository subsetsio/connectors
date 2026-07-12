-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "qatari_teams_associations",
    "non_qatari_teams_associations",
    "total_teams_associations",
    "qatari_clubs",
    "non_qatari_clubs",
    "total_clubs",
    "qatari_total",
    "non_qatari_total",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-sports-team-officials-accredited-in-sports-federations-by-activity-place-of-work-and-nationality-2023"
