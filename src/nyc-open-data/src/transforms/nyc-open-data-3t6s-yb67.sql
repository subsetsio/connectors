-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_id",
    "program_name",
    "program_aka",
    "umbrella",
    "collaborating_agencies",
    "program_description",
    "program_website",
    "plain_language_eligibility",
    "mandated_program",
    "how_to_apply",
    "agency_name"
FROM "nyc-open-data-3t6s-yb67"
