-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are country-week-source-variant observations; total case and sequencing denominators repeat across variants within the same country-week-source.
SELECT
    "country",
    "country_code",
    "year_week",
    "source",
    CAST("new_cases" AS BIGINT) AS new_cases,
    CAST("number_sequenced" AS BIGINT) AS number_sequenced,
    CAST("percent_cases_sequenced" AS DOUBLE) AS percent_cases_sequenced,
    "valid_denominator",
    "variant",
    CAST("number_detections_variant" AS BIGINT) AS number_detections_variant,
    CAST("number_sequenced_known_variant" AS BIGINT) AS number_sequenced_known_variant,
    CAST("percent_variant" AS DOUBLE) AS percent_variant
FROM "global-health-omicron-europe"
