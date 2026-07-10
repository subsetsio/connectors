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
    "cohort",
    "breakdown_topic",
    "breakdown",
    "ofqual_tier_1",
    "ofqual_tier_2",
    CAST("institution_count" AS BIGINT) AS institution_count,
    "entries_count",
    "entries_pass_count",
    "entries_pass_percent"
FROM "dfe-019d9136-a337-7773-8d2a-761a38292c3f"
