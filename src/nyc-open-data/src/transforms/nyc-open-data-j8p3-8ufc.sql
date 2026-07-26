-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "application_number",
    "orgname",
    "fy10_programs"
FROM "nyc-open-data-j8p3-8ufc"
