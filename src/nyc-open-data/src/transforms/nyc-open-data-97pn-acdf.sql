-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "age",
    "_2010" AS 2010,
    "_2015" AS 2015,
    "_2020" AS 2020,
    "_2025" AS 2025,
    "_2030" AS 2030,
    "_2035" AS 2035,
    "_2040" AS 2040
FROM "nyc-open-data-97pn-acdf"
