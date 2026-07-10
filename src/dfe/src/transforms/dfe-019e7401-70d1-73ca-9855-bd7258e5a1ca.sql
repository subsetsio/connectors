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
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "pcon_name",
    "pcon_code",
    "class_type",
    "class_size",
    CAST("class_count" AS BIGINT) AS class_count,
    CAST("pupil_count" AS BIGINT) AS pupil_count,
    "class_size_average"
FROM "dfe-019e7401-70d1-73ca-9855-bd7258e5a1ca"
