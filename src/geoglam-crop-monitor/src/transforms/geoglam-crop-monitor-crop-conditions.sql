-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No natural key: a row is one crop-growing-area polygon's assessment for a month, but the geometry (and the source's polygon id) are not published, so the same (period, country, region, crop) recurs across distinct overlapping polygons — often with DIFFERENT `conditions`/`drivers`. Never assume one row per (region, crop, month); treat each row as an independent polygon-level assessment and do not dedupe on the descriptive columns.
-- caution: The `conditions` classification is a qualitative ordinal label (Exceptional/Favourable/Watch/Poor/Failure/No Data plus blank markers), not a numeric measure — never sum or average it; count rows per class instead.
-- caution: `period` is a YYYYMM string stamped from the source layer name (the assessment month), not a row-level date; every row in a layer shares its period.
SELECT
    CAST("period" AS BIGINT) AS period,
    "country",
    "region",
    "crop",
    "conditions",
    "drivers"
FROM "geoglam-crop-monitor-crop-conditions"
