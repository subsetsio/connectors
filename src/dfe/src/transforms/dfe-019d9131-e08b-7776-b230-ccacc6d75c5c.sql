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
    "establishment_type",
    "sex",
    "exam_cohort",
    "value_added",
    "entries_count"
FROM "dfe-019d9131-e08b-7776-b230-ccacc6d75c5c"
