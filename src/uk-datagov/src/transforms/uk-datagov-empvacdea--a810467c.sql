-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are PxStat observations for a district-electoral-area geography; use the geography column before aggregating across areas.
SELECT
    "package_name",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_url",
    "source_row_number",
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial Year" AS financial_year,
    "DEA2014" AS dea2014,
    "District Electoral Area" AS district_electoral_area,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "uk-datagov-empvacdea--a810467c"
