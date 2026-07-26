-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "nta_class",
    "nta_code",
    "nta_name",
    "score_code",
    "score_name",
    "score_value"
FROM "nyc-open-data-dpq6-sy7w"
