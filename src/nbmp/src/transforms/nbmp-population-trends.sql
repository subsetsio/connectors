-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include both short_term and long_term summaries; filter term before comparing trend percentages.
-- caution: Trend percentages and confidence limits are not additive across species, countries, survey types, or terms.
SELECT
    "country",
    "species",
    "survey_type",
    "term",
    TRY_CAST("average_number_of_sites" AS INTEGER) AS average_number_of_sites,
    TRY_CAST("trend_pct_change" AS DOUBLE) AS trend_pct_change,
    TRY_CAST("lower_confidence_limit" AS DOUBLE) AS lower_confidence_limit,
    TRY_CAST("upper_confidence_limit" AS DOUBLE) AS upper_confidence_limit,
    "significance_of_change"
FROM "nbmp-population-trends"
