-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Census year" AS census_year,
    "NIROI" AS niroi,
    "Ireland and Northern Ireland" AS ireland_and_northern_ireland,
    CAST("UNPAID_CARE_AGG5" AS BIGINT) AS unpaid_care_agg5,
    "Provision of unpaid care" AS provision_of_unpaid_care,
    "AGE_BAND_AGG18" AS age_band_agg18,
    "Age (18 cats)" AS age_18_cats,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-cpni28"
