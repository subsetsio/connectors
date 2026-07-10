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
    "sex",
    "phonics_mark",
    CAST("expected_standard_pupil_count" AS BIGINT) AS expected_standard_pupil_count,
    "cumulative_percentage",
    "average_mean_phonics_mark"
FROM "dfe-b3bd9901-88ea-8575-aa70-579c2636caf4"
