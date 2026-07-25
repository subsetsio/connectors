-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cube_id",
    "series_key",
    "series_label",
    "dimensions_json",
    "frequency",
    "unit",
    CAST("scale" AS BIGINT) AS scale,
    "period",
    "period_start",
    "value"
FROM "swiss-national-bank-zast-snb.iea.bopc.1.ab.000000"
