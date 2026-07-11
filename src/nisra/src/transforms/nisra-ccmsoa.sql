-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(M1)" AS tlist_m1,
    "Month" AS month,
    "SOA" AS soa,
    "Super Output Area" AS super_output_area,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-ccmsoa"
