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
    "pcon_code",
    "pcon_name",
    CAST("nurseries_in_mainstream_schools_count" AS BIGINT) AS nurseries_in_mainstream_schools_count
FROM "dfe-019e8808-c9a4-7483-972c-ccfb11da6863"
