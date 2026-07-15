-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "patent_field_of_invention",
    "patent_grants",
    "rank"
FROM "sg-data-d-1a32f83189602167e67eb38bc0013efe"
