-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    "Urban_Rural" AS urban_rural,
    "Urban Rural" AS urban_rural_2,
    "Religion" AS religion,
    "Religion Label" AS religion_label,
    "Sex" AS sex,
    "Sex Label" AS sex_label,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-hca08"
