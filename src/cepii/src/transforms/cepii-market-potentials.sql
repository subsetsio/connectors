-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Market-potential source files carry different access concepts; filter by source_file before comparing values.
SELECT
    split_part(raw_line, ',', 1) AS source_file,
    split_part(raw_line, ',', 2) AS iso,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 3), '') AS BIGINT) AS year,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 4), '') AS DOUBLE) AS rmp_rv,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 5), '') AS DOUBLE) AS fmp_rv,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 6), '') AS DOUBLE) AS rmp_hm,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 7), '') AS DOUBLE) AS fmp_hm,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 8), '') AS DOUBLE) AS rmp_iv1,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 9), '') AS DOUBLE) AS rmp_iv2,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 10), '') AS DOUBLE) AS gdp_cap,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 11), '') AS DOUBLE) AS avgyrs,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 12), '') AS DOUBLE) AS lrmp_rv,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 13), '') AS DOUBLE) AS lfmp_rv,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 14), '') AS DOUBLE) AS lrmp_hm,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 15), '') AS DOUBLE) AS lfmp_hm,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 16), '') AS DOUBLE) AS lrmp_iv1,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 17), '') AS DOUBLE) AS lrmp_iv2,
    TRY_CAST(NULLIF(split_part(raw_line, ',', 18), '') AS DOUBLE) AS lgcap
FROM (
    SELECT
        "source_file,iso,year,RMP_RV,FMP_RV,RMP_HM,FMP_HM,RMP_IV1,RMP_IV2,gdpcap,avgyrs,lrmp_rv,lfmp_rv,lrmp_hm,lfmp_hm,lrmp_iv1,lrmp_iv2,lgcap" AS raw_line
    FROM "cepii-market-potentials"
)
