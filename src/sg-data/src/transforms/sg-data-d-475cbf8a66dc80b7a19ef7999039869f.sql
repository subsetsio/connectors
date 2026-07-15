-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_of_occurrence",
    "accident_incident",
    "type_of_aircraft",
    "description",
    "url"
FROM "sg-data-d-475cbf8a66dc80b7a19ef7999039869f"
