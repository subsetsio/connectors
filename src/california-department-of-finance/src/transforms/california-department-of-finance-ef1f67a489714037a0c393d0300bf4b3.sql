-- authored pass-through for a 2026-07-26 accept expansion (recollect
-- adopted the DRU 2015-25 wildfire vintage): same faithful-pass-through
-- contract as `hardened compile-transforms` output. Verified pure casts
-- only, no data fixes. Regenerate via model-verify + compile-transforms
-- once this raw is profiled; durable edits belong in the model stage.
SELECT
    CAST("OBJECTID" AS BIGINT) AS objectid,
    CAST("Shape__Are" AS DOUBLE) AS shape_are,
    CAST("Shape__Len" AS DOUBLE) AS shape_len,
    "County" AS county,
    "JOINNAME" AS joinname,
    "Banner" AS banner,
    "JurYr" AS juryr,
    "Year" AS year,
    CAST("Year123" AS BIGINT) AS year123,
    CAST("Pop" AS BIGINT) AS pop,
    CAST("HUStock" AS BIGINT) AS hustock,
    CAST("SFStock" AS BIGINT) AS sfstock,
    CAST("MFStock" AS BIGINT) AS mfstock,
    CAST("MHUStock" AS BIGINT) AS mhustock,
    CAST("SFLossAn" AS BIGINT) AS sflossan,
    CAST("MHULossAn" AS BIGINT) AS mhulossan,
    CAST("MFLossAn" AS BIGINT) AS mflossan,
    CAST("TotalLossAN" AS BIGINT) AS totallossan,
    CAST("SFStockLoss" AS DOUBLE) AS sfstockloss,
    CAST("MHUStockLoss" AS DOUBLE) AS mhustockloss,
    CAST("MHStockLoss" AS DOUBLE) AS mhstockloss,
    CAST("TotalStockLoss" AS DOUBLE) AS totalstockloss,
    CAST("SFLossDec" AS BIGINT) AS sflossdec,
    CAST("MHULossDec" AS BIGINT) AS mhulossdec,
    CAST("MFLossDec" AS BIGINT) AS mflossdec,
    CAST("TotalLossDec" AS BIGINT) AS totallossdec,
    CAST("Filter" AS BIGINT) AS filter,
    CAST("Sort" AS BIGINT) AS sort,
    "AnnualStockSF" AS annualstocksf,
    "AnnualStockMHU" AS annualstockmhu,
    "AnnualStockMF" AS annualstockmf,
    "AnnualStockTotal" AS annualstocktotal,
    "yr" AS yr,
    CAST("AdjustedAnnualLoss" AS BIGINT) AS adjustedannualloss
FROM "california-department-of-finance-ef1f67a489714037a0c393d0300bf4b3"
