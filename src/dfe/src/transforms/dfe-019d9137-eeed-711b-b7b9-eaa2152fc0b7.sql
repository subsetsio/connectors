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
    "breakdown_topic",
    "breakdown",
    "subject_combination",
    "maths_science_count",
    "subject_combination_only_count",
    "subject_combination_and_other_subject_count",
    "subject_combination_only_percent",
    "subject_combination_and_other_subject_percent"
FROM "dfe-019d9137-eeed-711b-b7b9-eaa2152fc0b7"
