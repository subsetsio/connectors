-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time" AS BIGINT) AS time,
    "classiication",
    "income_quintile_share_ratio_s80_s20",
    "gini_coefficient_of_equivalised_disposable_income"
FROM "statistics-austria-ogd-unglsilc02-hvd-ung-1"
