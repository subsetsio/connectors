-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are PxStat observations for a local-government-district geography; use the geography column before aggregating across areas.
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
    "LGD2014" AS lgd2014,
    "Local Government District" AS local_government_district,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "uk-datagov-empvaclgd--e1dbea89"
