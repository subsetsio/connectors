-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Grouped year" AS grouped_year,
    CAST("SEX" AS BIGINT) AS sex,
    "Sex Label" AS sex_label,
    "UR2015" AS ur2015,
    "Urban Rural" AS urban_rural,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-dfleurbrur"
