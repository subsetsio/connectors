-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "version",
    "establishment_type_group",
    "qualification_type",
    "subject",
    "test_year",
    CAST("number_entries" AS BIGINT) AS number_entries,
    "percentage"
FROM "dfe-1ae39901-a99d-e576-86d9-a376eff7f9af"
