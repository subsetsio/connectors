-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an aggregate reference-glacier series, not individual glacier observations.
SELECT
    "Year" AS year,
    "MB_REF_count" AS mb_ref_count,
    "REF_regionAVG" AS ref_regionavg,
    "REF_regionAVG_cum-rel-1970" AS ref_regionavg_cum_rel_1970
FROM "wgms-mb-ref"
