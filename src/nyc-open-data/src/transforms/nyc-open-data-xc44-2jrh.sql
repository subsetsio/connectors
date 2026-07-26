-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_dbn",
    "date",
    CAST("schoolyear" AS BIGINT) AS schoolyear,
    CAST("enrolled" AS BIGINT) AS enrolled,
    CAST("present" AS BIGINT) AS present,
    CAST("absent" AS BIGINT) AS absent,
    CAST("released" AS BIGINT) AS released
FROM "nyc-open-data-xc44-2jrh"
