-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "health_topic",
    "population",
    "indicator",
    "unit",
    CAST("geo_level" AS BIGINT) AS geo_level,
    "time_unit",
    "time",
    "region_code",
    "region_name",
    "num_value",
    "txt_value"
FROM "ecdc-infl-current-infl-flunews"
