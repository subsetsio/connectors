-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "release_year",
    "source_file",
    "variable_code",
    "series_kind",
    "country_code",
    "iso",
    "country",
    "observation_year",
    "value",
    CAST("value_text" AS DOUBLE) AS value_text,
    "has_missing_value_codes",
    "source_column"
FROM "yale-epi-2026-raw-data-with-missing-value-codes"
