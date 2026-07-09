-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "cv",
    "ci",
    CAST("calendar_years" AS BIGINT) AS calendar_years,
    CAST("time" AS BIGINT) AS time,
    "administrative_geography",
    "geography",
    "sexual_orientation",
    "sexualorientation",
    "unit_of_measure",
    "unitofmeasure"
FROM "ons-sexual-orientation-by-region"
