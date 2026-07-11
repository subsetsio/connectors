-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(M1)" AS tlist_m1,
    "Month" AS month,
    "TUMOURSITE" AS tumoursite,
    "Site of Tumour" AS site_of_tumour,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-cwt31tumour"
