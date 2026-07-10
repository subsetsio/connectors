-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "State/Territory" AS state_territory,
    "Counties_Served" AS counties_served,
    "Site" AS site,
    CAST("Population_Served" AS BIGINT) AS population_served,
    "Source" AS source,
    CAST("Site_WVAL" AS DOUBLE) AS site_wval,
    "Site_WVAL_Category" AS site_wval_category,
    strptime("Date_Included_In_WVAL", '%Y-%m-%d')::DATE AS date_included_in_wval,
    strptime("Week_End", '%Y-%m-%d')::DATE AS week_end,
    "Pathogen_Target" AS pathogen_target,
    CAST("date_updated" AS TIMESTAMP) AS date_updated
FROM "cdc-atcp-73re"
