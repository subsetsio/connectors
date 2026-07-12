-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activit_ar",
    "intl_qatari",
    "intl_nonqatari",
    "first_qatari",
    "first_nonqatari",
    "second_qatari",
    "second_nonqatari",
    "third_qatari",
    "third_nonqatari",
    "total_qatari",
    "total_nonqatari"
FROM "qatar-planning-and-statistics-authority-referees-accredited-in-the-sports-federations-by-sports-activity-grades-and-nationality-2023"
