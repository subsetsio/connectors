-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw workbook extract contains duplicate rows with the same geography, geo_level, year, measure, and value; treat rows as keyless observations and deduplicate in analysis if required.
-- caution: Rows may mix national, regional, state, capital, or other geography aggregation levels; filter geo_level before aggregating across geography.
SELECT
    "geography",
    "geo_level",
    "year",
    "measure",
    "value"
FROM "forum-brasileiro-seguranca-mortes-violentas-intencionais"
