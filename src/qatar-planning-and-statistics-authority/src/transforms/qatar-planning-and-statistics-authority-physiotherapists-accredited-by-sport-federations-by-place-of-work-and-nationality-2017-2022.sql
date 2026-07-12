-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "teams_qataris",
    "teams_nonqataris",
    "clubs_qataris",
    "clubs_nonqataris"
FROM "qatar-planning-and-statistics-authority-physiotherapists-accredited-by-sport-federations-by-place-of-work-and-nationality-2017-2022"
