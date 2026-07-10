-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "time_frame",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "new_la_code",
    "la_name",
    "old_la_code",
    "education_phase",
    "persistent_absence_percent"
FROM "dfe-55629501-e98b-0c75-adba-f95a0cfbb5e9"
