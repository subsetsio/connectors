-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "program_name",
    "program_description",
    "program_details",
    "eligibility",
    "locations",
    "contact"
FROM "nyc-open-data-an6v-iuem"
