-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Ad-hoc Year" AS BIGINT) AS ad_hoc_year,
    "SOA" AS soa,
    "Super Output Area" AS super_output_area,
    CAST("CAD" AS BIGINT) AS cad,
    "Crime and Disorder" AS crime_and_disorder,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-nimdm17t7"
