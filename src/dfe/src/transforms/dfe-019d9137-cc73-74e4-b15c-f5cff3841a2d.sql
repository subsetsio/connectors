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
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "sex",
    "subject_combination",
    "maths_science_count",
    CAST("subject_combination_only_count" AS BIGINT) AS subject_combination_only_count,
    CAST("subject_combination_and_other_subject_count" AS BIGINT) AS subject_combination_and_other_subject_count,
    "subject_combination_only_percent",
    "subject_combination_and_other_subject_percent"
FROM "dfe-019d9137-cc73-74e4-b15c-f5cff3841a2d"
