-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table mixes annual, quarterly, and higher-frequency indicators across WAEMU member states and the UEMOA aggregate; filter frequency and locality before aggregating values.
-- caution: Some source observations are duplicated exactly for the same series, locality, country, frequency, and date; de-duplicate before calculations that require one row per observation.
SELECT
    "locality",
    "country",
    "frequency",
    "series_code",
    "label",
    "sector",
    "subsector",
    "unit",
    "magnitude",
    "source",
    "series_type",
    "method",
    "period",
    "date",
    "value"
FROM "bceao-values"
